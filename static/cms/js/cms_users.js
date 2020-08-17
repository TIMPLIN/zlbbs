
$(function () {
    var submitBtn = $('.submit-delete-cuser');
    submitBtn.click(function (event) {
        event.preventDefault();
        var self = $(this);
        var cuser_id = self.attr('data-cuser-pk');
        zlalert.alertConfirm({
            'msg': '确定删除该用户?',
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/delete_cuser/',
                    'data': {
                        'cuser_id': cuser_id
                    },
                    'success': function (data) {
                        if(data['code'] === 200){
                            window.location.reload();
                        }else{
                            zlalert.alertInfo(data['message']);
                        }
                    },
                    'fail': function (error) {
                        zlalert.alertNetworkError();
                    }
                });
            }
        });
    });
});