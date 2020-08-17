/**
 * Created by hynev on 2017/12/29.
 */

$(function () {
    $("#add-board-btn").click(function (event) {
        event.preventDefault();
        zlalert.alertOneInput({
            'text':'请输入板块名称！',
            'placeholder': '板块名称',
            'confirmCallback': function (inputValue) {
                zlajax.post({
                    'url': '/cms/aboard/',
                    'data': {
                        'name': inputValue
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


$(function () {
    $(".edit-board-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr('data-name');
        var board_id = tr.attr("data-id");

        zlalert.alertOneInput({
            'text': '请输入新的板块名称！',
            'value': name,
            'confirmCallback': function (inputValue) {
                zlajax.post({
                    'url': '/cms/uboard/',
                    'data': {
                        'board_id': board_id,
                        'name': inputValue
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


$(function () {
    $('.delete-board-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var board_id = tr.attr('data-id');

        zlalert.alertConfirm({
            'msg': '确定删除该板块吗？',
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dboard/',
                    'data': {
                        'board_id': board_id
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