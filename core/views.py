import cv2
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from core.forms import VideoUploadForm
from core.models import VideoFile, WTV2D_data
from TV2D import TV2D

# Create your views here.


def home(request):
    wtv2d_data = WTV2D_data.objects.first()
    # For control processing videos some workers should be used like Celery
    # if wtv2d_data.processing:
    #     context = {'processing': True}
    #     return render(request, 'core/home.html', context)
    form = VideoUploadForm()
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            wtv2d_data.processing = True
            wtv2d_data.save()
            video_file = VideoFile(file=request.FILES['file'])
            video_file.status = VideoFile.VideoFileStatus.NEW.value
            video_file.save()

            video = cv2.VideoCapture(video_file.file.path)
            video_file.fps = video.get(cv2.CAP_PROP_FPS)
            video_file.video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            video_file.video_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            video_file.status = VideoFile.VideoFileStatus.PROCESSING.value
            video_file.save()

            # object_detection_model_path = "COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"
            object_detection_model_path = "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
            # Same as model by for now for config. If you use model from local sotrage you can still use config
            ## from Detectron2 Model Zoo and Baselines.
            # object_detection_config_path = "COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"
            object_detection_config_path = "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
            homography_keypoint_path = "TV2D/models/FPN_efficientnetb3_0.0001_4.h5"
            homography_deephomo_path = "TV2D/models/HomographyModel_0.0001_4.h5"
            deep_sort_model = "TV2D/models/market_bot_R50.pth"
            deep_sort_model_config = "TV2D/deep_sort_pytorch/thirdparty/fast-reid/configs/Market1501/bagtricks_R50.yml"

            tv2d = TV2D.TV2D(object_detection_model_path, object_detection_config_path=object_detection_config_path,
                        homography_on=True, team_detection_on=True,
                        tracker_on=True, no_gui=True,
                        homography_pretreined=False, homography_deephomo_path=homography_deephomo_path,
                        homography_keypoint_path=homography_keypoint_path,
                        deep_sort_model_path=deep_sort_model, deep_sort_model_config=deep_sort_model_config)
            output_video_name = ".".join(video_file.file.name.split(".")[:-1]) + "_" + str(video_file.pk) + ".mkv"
            export_data_file_path = ".".join(video_file.file.name.split(".")[:-1]) + "_" + str(video_file.pk) + ".csv"
            video_file.output_file = output_video_name
            video_file.csv_file = export_data_file_path
            video_file.save()
            tv2d(TV2D.TV2D.RunOn.VIDEO, video_file.file.path, export_output_path=f"media/{output_video_name}",
                 export_data_file_path=f"media/{export_data_file_path}")
            video_file.status = VideoFile.VideoFileStatus.READY.value
            video_file.save()
        else:
            messages.error(request, "Something went wrong")

    wtv2d_data.processing = False
    wtv2d_data.save()
    context = {'form': form}
    return render(request, 'core/home.html', context)

def video_list_view(request):
    videos = VideoFile.objects.all().order_by("-pk")
    context = {'videos': videos, 'enum_video_file_status': VideoFile.VideoFileStatus}
    return render(request, 'core/video_list.html', context)
