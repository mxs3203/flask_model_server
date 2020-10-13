class Config(object):
    # XRay
    XRAY_IMAGE_UPLOADS = "recievedImgFolder/"
    XRAY_WEIGHTS = "runs/xray_airport_x/exp0_xray_airport_x/weights/best.pt"
    XRAY_AGNOSTIC_NMS = True
    XRAY_OUTPUT_FOLDER = "serverOutput/xray"
    XRAY_CONF_THRES = 0.5
    XRAY_IOU_THRES = 0.5

    # Coccidia
    COCCIDIA_IMAGE_UPLOADS = "recievedImgFolder/"
    COCCIDIA_WEIGHTS = "runs/yolom_coccidia/weights/best.pt"
    COCCIDIA_AGNOSTIC_NMS = True
    COCCIDIA_OUTPUT_FOLDER = "serverOutput/coccidia"
    COCCIDIA_CONF_THRES = 0.8
    COCCIDIA_IOU_THRES = 0.8

    # Neutrophil
    NEUTROPHIL_IMAGE_UPLOADS = "recievedImgFolder/"
    NEUTROPHIL_WEIGHTS = "runs/exp1_neutrophils_m_finetune/weights/best.pt"
    NEUTROPHIL_AGNOSTIC_NMS = True
    NEUTROPHIL_OUTPUT_FOLDER=  "serverOutput/neutrohpil"
    NEUTROPHIL_CONF_THRES = 0.7
    NEUTROPHIL_IOU_THRES = 0.7

    # DB
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost:3306/over_under'
