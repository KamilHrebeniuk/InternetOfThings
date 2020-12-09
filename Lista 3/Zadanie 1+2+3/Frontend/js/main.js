$(document).ready(function() {
    var $console = $("#console");
    var correct = "#009933";
    var alert = "#ffbc30";
    var error = "#a70000";

    function communicate (text, color) {
        return "<span style='color: " + color + "'>" + text + "</span>";
    }

    $("#register-button").click(function () {
        var port = $("#register-input").val();
        var breaker = false;

        $(".service-port").each(function (index, target) {
            if (target.innerText === port) {
                $console.prepend(communicate("Already connected to: " + port, alert));
                breaker = true;
            }
        })

        if (!breaker) {
            $.post(
                "http://127.0.0.1:" + port + "/register",
                function (result) {
                    $console.prepend(communicate("Connected on: " + port, correct));
                    result = JSON.parse(result);
                    var $root = $("#services-list");
                    var index = $(".service-wrapper").length;

                    $root.append(
                        "<div class='service-wrapper'>" +
                        "   <div class='service-name'>" + result.name + "</div> " +
                        "   <div class='service-port'>" + port + "</div> " +
                        "   <div class='service-status'>" + result.status + "</div>" +
                        "   <div class='service-communication'>" + result.communication + "</div>" +
                        "   <div class='service-buttons'>" +
                        "       <button class='service-off'>Change State</button> " +
                        "       <button class='service-change'>Change Communication</button> " +
                        "       <button class='service-power-up'>Power Up</button> " +
                        "       <button class='service-power-down'>Power Down</button> " +
                        "   </div>" +
                        "</div>")


                    $(".service-off").eq(index).click(function () {
                        $.post(
                            "http://127.0.0.1:" + $(".service-port").eq(index).text() + "/state-change",
                            function (result) {
                                result = JSON.parse(result);
                                $console.prepend(communicate("Device has been successfully " + result.state, correct));

                                var $service_status = $(".service-status").eq(index);
                                if (result.state === "Turned On") {
                                    $service_status.text("Working");
                                    $service_status.css("background-color", correct)
                                }
                                else if (result.state === "Turned Off") {
                                    $service_status.text("Ready");
                                    $service_status.css("background-color", alert)
                                }
                            })
                            .fail(function () {
                                $console.prepend(communicate("Failed to connect on: " + port, error));
                            });
                        return false;
                    })

                    $(".service-change").eq(index).click(function () {
                        $.post(
                            "http://127.0.0.1:" + $(".service-port").eq(index).text() + "/communication",
                            function (result) {
                                result = JSON.parse(result);
                                $console.prepend(communicate("Communication changed to: " + result.communication, correct));
                                $(".service-communication").eq(index).text(result.communication);
                            })
                            .fail(function () {
                                $console.prepend(communicate("Failed to connect on: " + port, error));
                            });
                        return false;
                    })

                    $(".service-power-up").eq(index).click(function () {
                        $.post(
                            "http://127.0.0.1:" + $(".service-port").eq(index).text() + "/power-up",
                            function (result) {
                                result = JSON.parse(result);
                                $console.prepend(communicate("Power raised to: " + result.power, correct));
                            })
                            .fail(function () {
                                $console.prepend(communicate("Failed to connect on: " + port, error));
                            });
                        return false;
                    })

                    $(".service-power-down").eq(index).click(function () {
                        $.post(
                            "http://127.0.0.1:" + $(".service-port").eq(index).text() + "/power-down",
                            function (result) {
                                result = JSON.parse(result);
                                $console.prepend(communicate("Power decreased to: " + result.power, correct));
                            })
                            .fail(function () {
                                $console.prepend(communicate("Failed to connect on: " + port, error));
                            });
                        return false;
                    })
                })
                .fail(function () {
                    $console.prepend(communicate("Failed to connect on: " + port, error));
                })
            return false;
        }
    })

    setInterval(function() {
        ask()
    }, 5000);

    function ask(){
        $(".service-port").each(function (index, target) {
            $.post(
                "http://127.0.0.1:" + target.innerText + "/status",
                function (result) {
                    result = JSON.parse(result);
                    $console.prepend(communicate("Device on: " + target.innerText + " is " + result.status, correct));
                    if (result.power) {
                        $console.prepend(communicate("Current device power is: " + result.power, correct));
                        $(".light").eq(index).css({"width": result.power * 2, "height": result.power * 2})
                    }
                    if (result.communication) {
                        $(".service-communication").eq(index).text(result.communication);
                    }
                    var $service_status = $(".service-status").eq(index);
                    $service_status.text(result.status);
                    if (result.status === "Working") {
                        $service_status.css("background-color", correct)
                    }
                    else if (result.status === "Ready") {
                        $service_status.css("background-color", alert)
                        $(".light").eq(index).css({"width": 0, "height": 0})
                    }
                })
                .fail(function () {
                    $console.prepend(communicate("Failed to connect on: " + target.innerText, error));
                    var $service_status = $(".service-status").eq(index);
                    $service_status.text("Failed");
                    $service_status.css("background-color", error)
                });
        })
    }
})