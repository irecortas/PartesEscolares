/** @odoo-module **/
import { ListController } from "@web/views/list/list_controller";
import { listView } from "@web/views/list/list_view";
import { registry } from "@web/core/registry";

export class AlumnoListController extends ListController {
    setup() {
        super.setup();
    }
    
    onImportXml() {
        this.actionService.doAction("partes_escolares.action_xml_import_wizard");
    }
    
    onExportXml() {
        this.actionService.doAction("partes_escolares.action_xml_export_wizard");
    }
}

registry.category("views").add("alumno_list_view_buttons", {
    ...listView,
    Controller: AlumnoListController,
    buttonTemplate: "partes_escolares.AlumnoListView.Buttons",
});
