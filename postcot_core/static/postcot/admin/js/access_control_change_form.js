$(document).ready( function () {
    let form = {};

    form._POSTFIX_IDENTIFIER_BODY_LOOKUP_TABLE = {
        // Postfix Identifier Body              Symbol Pattern
        "ccert":                                ["CLIENT",      "CERT",         false],
        "sasl":                                 ["CLIENT",      "SASL",         false],
        "client":                               ["CLIENT",      "HOSTNAME",     false],
        "client_${content}":                    ["CLIENT",      "{content}",    false],
        "reverse_client_host_name":             ["CLIENT",      "HOSTNAME",     true],
        "reverse_client_host_name_${content}":  ["CLIENT",      "{content}",    true],
        "helo":                                 ["HELO",        "HOSTNAME",     null],
        "helo_${content}":                      ["HELO",        "{content}",    null],
        "recipient":                            ["RECIPIENT",   "HOSTNAME",     null],
        "recipient_${content}":                 ["RECIPIENT",   "{content}",    null],
        "sender":                               ["SENDER",      "HOSTNAME",     null],
        "sender_${content}":                    ["SENDER",      "{content}",    null],
    };

    form._update_postfix_identifier = function() {
        let role_select = $("#id_subject_role");
        let content_select = $("#id_subject_content");
        let reverses_hostname_checkbox = $("#id_reverses_hostname");
        let postfix_identifier_input = $("#id_postfix_identifier");

        let role = role_select.val();
        let content = content_select.val();
        let reverses_hostname = reverses_hostname_checkbox.is(':checked');

        let identifier = this._make_postfix_identifier(role, content, reverses_hostname);

        if (identifier != null) {
            postfix_identifier_input.val(identifier);
        } else {
            postfix_identifier_input.val("");
        }

        console.log([role, content, reverses_hostname, identifier].join(" "));
    };

    form._make_postfix_identifier = function(
        role, content, reverses_hostname
    ) {
        let body = this._make_postfix_identifier_body(
            role,
            content,
            reverses_hostname
        );

        if (body != null) {
            return 'check_' + body + '_access';
        }

        return null;
    };

    form._make_postfix_identifier_body = function(
        role, content, reverses_hostname
    ) {
        let symbols = [role, content, reverses_hostname];

        for (let body_template in this._POSTFIX_IDENTIFIER_BODY_LOOKUP_TABLE) {
            console.log(body_template);

            let symbol_pattern = this._POSTFIX_IDENTIFIER_BODY_LOOKUP_TABLE[body_template];

            let body = body_template;

            let mismatched = false;

            let index = 0;

            while (index < symbols.length && !mismatched) {
                let symbol = symbols[index];
                let pattern = symbol_pattern[index];

                if (symbol === pattern) {
                    console.log("1: " + symbol + " == " + pattern);
                    // do nothing
                } else if (pattern != null && pattern.constructor.name === "String" && pattern.match("^{\.+}$")) {
                    // interpolatable pattern
                    console.log("2: " + symbol + " =~ " + pattern);
                    let symbol_content = this._make_postfix_identifier_component_for_symbol(symbol);
                    if (symbol_content != null) {
                        body = body.replace("$" + pattern, symbol_content);
                    } else {
                        mismatched = true;
                    }
                } else if (pattern == null) {
                    console.log("N: " + symbol + " is null");
                } else {
                    console.log("4: " + symbol + " != " + pattern);
                    mismatched = true;
                }

                index += 1;
            }

            if (!mismatched) {
                return body;
            }
        }

        return null;
    };

    form._make_postfix_identifier_component_for_symbol = function(symbol) {
        console.log(symbol);
        switch (symbol) {
            case "CERT":
                return null;
            case "HOSTNAME":
                return null;
            case "A_RECORD":
                return "a";
            case "NS_RECORD":
                return "ns";
            case "MX_RECORD":
                return "mx";
            case "SASL":
                return null;
        }
    };

    form._update_reverses_hostname_visibility = function() {
        let reverses_hostname_field = $("div.field-box.field-reverses_hostname");

        let role_select = $("#id_subject_role");
        let content_select = $("#id_subject_content");

        let role = role_select.val();
        let content = content_select.val();

        if (this._can_reverse_hostname(role, content)) {
            reverses_hostname_field.show();
        } else {
            reverses_hostname_field.hide();
        }
    };

    form._can_reverse_hostname = function(role, content) {
        if (role === 'CLIENT') {
            let allowed_contents = new Set([
                'HOSTNAME', 'A_RECORD', 'NS_RECORD', 'MX_RECORD'
            ]);

            if (allowed_contents.has(content)) {
                return true;
            }
        }
        return false;
    };
    form._update_reverses_hostname_visibility();
    form._update_postfix_identifier();

    $("#id_subject_role").change(function() {
        form._update_reverses_hostname_visibility();
        form._update_postfix_identifier();
    });

    $("#id_subject_content").change(function() {
        form._update_reverses_hostname_visibility();
        form._update_postfix_identifier();
    });

    $("#id_reverses_hostname").click(function() {
        form._update_postfix_identifier();
    });
});
