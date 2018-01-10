$(function() {

    jQuery.validator.addMethod("alphacharactersOnly", function(value, element) {
        re = /^[a-zA-Z&\s]*$/;
        return this.optional(element) || re.test(value);
    }," Please enter characters only.");

    iban_id = $("#id_hidden_id").val();

    $("form[id='iban_create']").validate({
        errorElement: "div",
        errorPlacement: function(error, element) {
            $("span.error.text-danger").hide();
            error.insertAfter(element);
        },
        rules: {
            first_name:{
                required:true,
                minlength:3,
                maxlength:80,
                alphacharactersOnly : true,
            },
            last_name:{
                required:true,
                minlength:3,
                maxlength:80,
                alphacharactersOnly : true,            
            },
            iban_number:{
                required:true,
                iban:true,
                minlength:4,
                maxlength:80,
                remote:{
                    url:"/unique/iban/",
                    type:"post",
                    dataType: "json",
                    data:{"csrfmiddlewaretoken":$("input[name='csrfmiddlewaretoken']").val(),
                            "iban_id":iban_id
                        }
                    }
            },
        },
        messages: {
            first_name:{
                required:"Please Enter First Name.",
                minlength:"Minimum 3 characters required.",
                maxlength:"Minimum 80 characters allowed.",
                alphacharactersOnly:"Please enter characters only.",            
            },
            last_name:{
                required:"Please Enter Last Name.",
                minlength:"Minimum 3 characters required.",
                maxlength:"Minimum 80 characters allowed.",
                alphacharactersOnly:"Please enter characters only.",
            },
            iban_number:{
                required:"Please Enter Iban number.",
                iban:"Please specify a valid IBAN",
                minlength:"Minimum 4 characters required.",
                maxlength:"Maximum 80 characters allowed.",
                remote:"Iban number is already added."
            }
        }
    });
});