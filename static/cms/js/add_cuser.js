/**
 * Created by hynev on 2017/11/30.
 */

$(function () {
    $("#add-cuser").click(function (event) {
        event.preventDefault();
        var email = $("input[name='email']").val();
        if(!email){
            zlalert.alertInfoToast('请输入邮箱');
            return;
        }
        zlajax.get({
            'url': '/cms/add_cuser/',
            'data': {
                'email': email
            },
            'success': function (data) {
                if(data['code'] === 200){
                    window.location = '/cms/cusers/'
                }else{
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });
    });
});

