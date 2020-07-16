# coding:utf-8
import IPython
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64
from IPython.display import display, Javascript
from kerasyolo3.yolo import YOLO
import argparse

from google.colab import output


def use_cam(quality=0.2):
    js = Javascript('''
    async function useCam(quality) {
        const div = document.createElement('div');
        document.body.appendChild(div);
        //video element
        const video = document.createElement('video');
        video.style.display = 'None';
        const stream = await navigator.mediaDevices.getUserMedia({video: true});
        div.appendChild(video);
        video.srcObject = stream;
        await video.play();

        //canvas for display. frame rate is depending on display size and jpeg quality.
        display_size = 320 
        const src_canvas = document.createElement('canvas');
        src_canvas.width  = display_size;
        src_canvas.height = display_size * video.videoHeight / video.videoWidth;
        const src_canvasCtx = src_canvas.getContext('2d');
        src_canvasCtx.translate(src_canvas.width, 0);
        src_canvasCtx.scale(-1, 1);
        div.appendChild(src_canvas);

        const dst_canvas = document.createElement('canvas');
        dst_canvas.width  = src_canvas.width;
        dst_canvas.height = src_canvas.height;
        const dst_canvasCtx = dst_canvas.getContext('2d');
        div.appendChild(dst_canvas);

        //exit button
        const btn_div = document.createElement('div');
        document.body.appendChild(btn_div);
        const exit_btn = document.createElement('button');
        exit_btn.textContent = 'Exit';
        var exit_flg = true
        exit_btn.onclick = function() {exit_flg = false};
        btn_div.appendChild(exit_btn);

            // Resize the output to fit the video element.
            google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

            var send_num = 0
            // loop
            _canvasUpdate();
            async function _canvasUpdate() {
                src_canvasCtx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, src_canvas.width, src_canvas.height);     
                if (send_num<1){
                    send_num += 1
                    const img = src_canvas.toDataURL('image/jpeg', quality);
                    const result = google.colab.kernel.invokeFunction('notebook.run', [img], {});
                    result.then(function(value) {
                        parse = JSON.parse(JSON.stringify(value))["data"]
                        parse = JSON.parse(JSON.stringify(parse))["application/json"]
                        parse = JSON.parse(JSON.stringify(parse))["img_str"]
                        var image = new Image()
                        image.src = parse;
                        image.onload = function(){dst_canvasCtx.drawImage(image, 0, 0)}
                        send_num -= 1
                    })
                }
                if (exit_flg){
                    requestAnimationFrame(_canvasUpdate);   
                }else{
                    stream.getVideoTracks()[0].stop();
                }
            };
        }
        ''')
    display(js)
    data = output.eval_js('useCam({})'.format(quality))


def run(img_str):
    # decode to image
    decimg = base64.b64decode(img_str.split(',')[1], validate=True)
    decimg = Image.open(BytesIO(decimg))
    decimg = np.array(decimg, dtype=np.uint8)
    decimg = cv2.cvtColor(decimg, cv2.COLOR_BGR2RGB)

    #############your process###############

    out_img = decimg

    #############your process###############

    # encode to string
    _, encimg = cv2.imencode(
        ".jpg", out_img, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    img_str = encimg.tostring()
    img_str = "data:image/jpeg;base64," + \
        base64.b64encode(img_str).decode('utf-8')
    return IPython.display.JSON({'img_str': img_str})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument(
        '--model', type=str,
        help='path to model weight file, default ' +
        YOLO.get_defaults("model_path")
    )
    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' +
        YOLO.get_defaults("anchors_path")
    )
    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' +
        YOLO.get_defaults("classes_path")
    )
    FLAGS = parser.parse_args()
    yolo = YOLO(**vars(FLAGS))

    output.register_callback('notebook.run', run)

    use_cam()
