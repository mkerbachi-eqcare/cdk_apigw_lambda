'use strict';
console.log('Loading hello world function');


exports.handler = async (event) => {
    console.log("request: " + JSON.stringify(event));
    const responseCode = 200;
    let responseBody = {
        message: "Hellow World!",
        input: event
    };
    let response = {
        statusCode: responseCode,
        headers: {
            "x-custom-header" : "my custom header value"
        },
        body: JSON.stringify(responseBody)
    };
    return response;
}



// exports.handler = function (event, context) {
//     console.log("EVENT: \n" + JSON.stringify(event, null, 2))
//     return context.logStreamName
// }