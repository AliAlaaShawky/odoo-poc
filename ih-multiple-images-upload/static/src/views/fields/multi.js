/** @odoo-module **/

import { X2ManyField } from '@web/views/fields/x2many/x2many_field';
import { FormArchParser } from "@web/views/form/form_arch_parser";
import { useEnv } from "@odoo/owl";
import { session } from "@web/session";
import { formatFloat } from "@web/views/fields/formatters";
import { patch } from '@web/core/utils/patch';
import { useService } from "@web/core/utils/hooks";
import { makeContext } from "@web/core/context";
import { loadSubViews } from "@web/views/form/form_controller";
import { getDataURLFromFile } from "@web/core/utils/urls";
import { createElement, parseXML } from "@web/core/utils/xml";


const DEFAULT_MAX_FILE_SIZE = 128 * 1024 * 1024;

patch(X2ManyField.prototype, {
    setup() {
        super.setup(...arguments);
        this.pmiNotificationService = useService('notification');
        this.pmiUiService = useService('ui');
        this.pmiuViewService = useService('view');
        this.pmiuUserService = useService('user');
        this.pmiuEnv = useEnv();
    },

    get isProductMultipleImagesUpload() {
        return this.viewMode === 'kanban' && this.activeField.options?.multiple_images_upload;
    },

    get maxUploadSize() {
        return session.max_file_upload_size || DEFAULT_MAX_FILE_SIZE;
    },

async onAddMultipleImages(event) {
    const input = event.target;
    const files = [...input.files];
    input.value = null;
    if (!files) {
        return;
    }
    let promises = [];
    let errors = [];
    this.pmiUiService.block();

    files.forEach(file => {
        if (file.size > this.maxUploadSize) {
            const maxFileSizeStr = formatFloat(this.maxUploadSize, { humanReadable: true });
            errors.push(`${file.name} file exceeds the maximum file size of ${maxFileSizeStr}.`);
            return;
        }

        // Add a file type check here
        if (!file.type.startsWith('image/')) {
            errors.push(`${file.name} is not a supported image file.`);
            return;
        }

        promises.push(new Promise(async (resolve, reject) => {
            try {
                const fileData = await getDataURLFromFile(file);
                let fileName = file.name;
                if (fileName.includes('.')) {
                    fileName = fileName.split('.')[0];
                }
                await this.addImage(fileName, fileData.split(',')[1]);
                resolve();  // Resolve the promise on success
            } catch (e) {
                // Improved error logging
                console.error(`Error when reading file: ${file.name}`, e);
                errors.push(`Error when reading ${file.name} file. Possible issue: ${e.message}`);
                reject(e);  // Reject the promise on error
            }
        }));
    });

    try {
        await Promise.all(promises);
    } catch (e) {
        console.error("One or more image uploads failed.", e);
    } finally {
        this.pmiUiService.unblock();
    }

    if (errors.length) {
        this.pmiNotificationService.add(
            errors.join('\n'),
            {
                title: 'Images upload',
                type: 'danger',
            }
        );
    }
},

    async addImage(name, imageData) {
        const form = await this.getFormViewInfo({
            list: this.list,
            activeField: this.activeField,
            viewService: this.pmiuViewService,
            userService: this.pmiuUserService,
            env: this.pmiuEnv,
        });

        const recordParams = {
            context: makeContext([this.list.context, {
                default_name: name,
                default_image_1920: imageData,
            }]),
            resModel: this.list.resModel,
            activeFields: form.activeFields,
            fields: { ...form.fields },
            views: { form },
            mode: 'edit',
            viewType: 'form',
        };

//        const record = await this.list.model.addNewRecord(this.list, recordParams);
       await this.list.addNewRecord(recordParams);
    },

    async getFormViewInfo({ list, context, activeField, viewService, userService, env }) {
        let formArchInfo = activeField.views.form;
        let fields = activeField.fields;
        const comodel = list.resModel;
        if (!formArchInfo) {
            const {
                fields: formFields,
                relatedModels,
                views,
            } = await viewService.loadViews({
                context: makeContext([list.context, context]),
                resModel: comodel,
                views: [[false, "form"]],
            });
            const xmlDoc = parseXML(views.form.arch);
            formArchInfo = new FormArchParser().parse(xmlDoc, relatedModels, comodel);
            fields = { ...list.fields, ...formFields };
        }

        await loadSubViews(
            formArchInfo.fieldNodes,
            fields,
            {}, // context
            comodel,
            viewService,
            userService,
            env.isSmall
        );

        return { archInfo: formArchInfo, fields };
    }
});
