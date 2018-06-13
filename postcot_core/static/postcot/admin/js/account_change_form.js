let sets_hashed_password = false;

$(document).ready( function () {
    $('#id_sets_hashed_password').ready( function() {
        sets_hashed_password = $(this).val();
    }).click( function () {
        sets_hashed_password = !sets_hashed_password;
        if (sets_hashed_password) {
            $('div.form-row.field-old_password').hide();
            $('#id_password').attr('type', 'text');
            $('#id_password_again').attr('type', 'text');
        } else {
            $('div.form-row.field-old_password').show();
            $('#id_password').attr('type', 'password');
            $('#id_password_again').attr('type', 'password');
        }
    });
});
