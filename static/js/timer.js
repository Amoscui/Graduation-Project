var value = 0;

$(function () {
    function increment( ) {

        $("#prog").css("width",value + "%").text(value + "%");
        if (value>=0 && value<=50) {
            $("#prog").addClass("progress-bar-success");
        }
        else if (value>=50 && value <=75) {
            $("#prog").removeClass("progress-bar-success");
            $("#prog").addClass("progress-bar-info");

        }
        else if (value>=75 && value <=90) {
            $("#prog").removeClass("progress-bar-info");
            $("#prog").addClass("progress-bar-warning");
        }
        else if(value >= 90 && value<100) {
            $("#prog").removeClass("progress-bar-warning");
            $("#prog").addClass("progress-bar-danger");
        }else{
            $('#btn').trigger("click");
            return ;
        }
        value += 1;
        st = setTimeout(increment,1000);
    }
    increment();
});