if (typeof tinyMCE != 'undefined') {
    tinymce.init({
        selector: ".mceEditor",
        relative_urls: false,
        height : 400,
        file_browser_callback: function (field_name, url, type, win) {
            var frame = tinyMCE.activeEditor.windowManager.open({
                file: window.__filebrowser_url + '?pop=2&type=' + type,
                width: 820,
                height: 500,
                resizable: "yes",
                scrollbars: "yes",
                inline: "yes",
                close_previous: "no"
            }, {
                window: win,
                input: field_name,
                editor_id: tinyMCE.editors[0].id
            });

            window.tinymce_activeEditor = tinyMCE.activeEditor;
            window.tinymce_activeFrame = frame;
            window.tinymce_activeInput = field_name;
            return false;
        },

        theme: "modern",
        plugins: [
            "advlist autolink lists link image charmap print preview hr anchor pagebreak",
            "searchreplace wordcount visualblocks visualchars code fullscreen",
            "insertdatetime media nonbreaking save table contextmenu directionality",
            "template paste caption"
        ],
        content_css: "/static/css/tinymce.css",

        toolbar1: "insertfile undo redo | styleselect | bold italic lineheight dropcaps blockquote | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image caption",
        toolbar2: "fullscreen print preview media | fontselect fontsizeselect forecolor backcolor",
        image_advtab: true,
        templates: [
            {title: 'Test template 1', content: 'Test 1'},
            {title: 'Test template 2', content: 'Test 2'}
        ],
        formats : {
            dropcaps: {inline: 'span', classes: "dropcaps"},
            lineheight: {block: 'p', styles: {'lineHeight': '%value'}},
            blockquote: {block: 'blockquote', classes: "blockquote"}
        },

        setup: function(ed) {
            ed.addButton('dropcaps', {
                text: 'Drop Caps',
                icon: false,
                onclick: function() {
                    ed.formatter.apply('dropcaps');
                }
            });
            ed.addButton('blockquote', {
                text: 'Blockquote',
                icon: false,
                onclick: function() {
                    ed.formatter.apply('blockquote');
                }
            });
            ed.addButton('lineheight', {
                text: 'Line height',
                icon: false,
                onclick: function() {
                    ed.windowManager.open({
                        title: 'Specify line height',
                        body: [
                            {type: 'textbox', name: 'lineheight', label: 'Value'}
                        ],
                        onsubmit: function(e) {
                            ed.formatter.apply('lineheight', {value: e.data.lineheight});
                        }
                    });
                }
            });
        }
    });

}