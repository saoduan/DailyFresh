/**
 * Created by Yi Chen on 2017/9/6.
 */
$(function () {
    var user_error = false;
    var pwd_error = false;
    var vc_error = false;

    $('#name_input').blur(function() {
        check_user();
	});

    $('#pass_input').blur(function () {
        check_pwd();
    })
    
    $('#verify').blur(function () {
        check_vc();
    })

    function check_user () {
        var len = $('#name_input').val().length;
        if(len == 0){
            user_error = true
            $('#user_error').html('用户名不允许为空').show();
        }
        else{
             $('#user_error').hide();
            $.get('/user/user_correct/?uname='+$('#name_input').val(),function (data){
                if(data.count == 1){
                    $('#user_error').hide();
                    user_error = false;
                }
                else
                {
                    $('#user_error').html('用户名不存在');
                    $('#user_error').show();
                    user_error = true;
                }
                });
        }
    }

    function check_pwd() {
        var len = $('#pass_input').val().length;
        if(len == 0) {
            pwd_error = true
            $('#pwd_error').html('密码不允许为空').show();
        }
        else{
             $('#pwd_error').hide();
            // $.get('/user/pwd_correct/?pwd='+$('#pass_input').val()+"&uname=" + $('#name_input').val(), function (data) {
            //     if(data.result == 1){
            //         $('#pwd_error').hide()
            //         pwd_error = false;
            //     }
            //     else{
            //         $('#pwd_error').html('密码错误');
            //         $('#pwd_error').show()
            //         pwd_error = true;
            //     }
            // });
            pwd_error = false;
        }

    }

    function check_vc() {
        var len = $('#verify').val().length;
        if(len == 0){
            $('#vc_error').html('请填写验证码').show();
            vc_error = true
        }
        else{
            $('#vc_error').hide()
            vc_error = false
        }
    }

    $('form').submit(function () {
        check_user();
        check_pwd();
        check_vc();
        if(user_error == false && pwd_error == false && vc_error == false){
            return true;
        }else{
            return false;
        }
    });
})