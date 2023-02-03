def process_check_result(self, check):
        self.last_check = check
        if check.result == RESULT_SUCCESS:
            print(_("Check succeeded: %s") % check.title)
            if check in self.checks:
                self.checks.remove(check)
                self.run_next_check()
        elif check.result == RESULT_EXCEPTION:
            print("An error occured, showing python traceback:")
            print(check.message)
            #exit() TODO
        else:
            #self.builder.get_object("upgrade_stack").set_visible_child_name("page_error")
            #self.builder.get_object("label_error_title").set_text(check.title)
            print(f"{bcolors.BOLD}{check.title}{bcolors.ENDC}")
            #self.builder.get_object("label_error_text").set_text(check.message)
            if check.result == RESULT_ERROR:
                print(_("Error: %s") % check.message, end=" ") # TODO really?
            elif check.result == RESULT_WARNING:
                print(_("Warning: %s") % check.mesage, end=" ") # TODO really?
            elif check.result == RESULT_INFO: # TODO or else?
                print(check.message)
                #okbutton true
                if check in self.checks:
                    self.checks.remove(check)
                if check.allow_recheck:
                    # ask for recheck todo
            self.builder.get_object("error_check_button").set_visible(check.allow_recheck) # TODO
            #self.builder.get_object("error_ok_button").set_visible(False)

            # Show info if any
            box_info = self.builder.get_object("box_info")
            for child in box_info.get_children():
                child.destroy()
            for info in check.info:
                if isinstance(info, str):
                    if info == "---":
                        widget = Gtk.Separator()
                    else:
                        widget = Gtk.Label()
                        widget.set_markup(info)
                        widget.set_line_wrap(True)
                elif isinstance(info, TableList):
                    widget = Gtk.ScrolledWindow()
                    widget.set_min_content_width(400)
                    widget.set_min_content_height(200)
                    widget.set_shadow_type(Gtk.ShadowType.IN)
                    treeview = Gtk.TreeView()
                    treeview.set_headers_visible(info.show_column_names)
                    widget.add(treeview)
                    index = 0
                    types = []
                    for name in info.columns:
                        column = Gtk.TreeViewColumn(name, Gtk.CellRendererText(), text=index)
                        treeview.append_column(column)
                        index += 1
                        types.append(str)
                    model = Gtk.ListStore()
                    model.set_column_types(types)
                    model.set_sort_column_id(0, Gtk.SortType.ASCENDING)
                    for value in info.values:
                        iter = model.insert_before(None, None)
                        index = 0
                        for subval in value:
                            model.set_value(iter, index, subval)
                            index += 1
                    treeview.set_model(model)
                box_info.pack_start(widget, False, False, 0)
                box_info.show_all()
            if len(check.info) > 0:
                self.builder.get_object("scroll_info").show_all()
            else:
                self.builder.get_object("scroll_info").hide()
            if check.message == "":
                self.builder.get_object("label_error_text").hide()
            else:
                self.builder.get_object("label_error_text").show()
            # Activate Fix button if appropriate
            self.builder.get_object("error_fix_button").set_visible(check.fix != None)
