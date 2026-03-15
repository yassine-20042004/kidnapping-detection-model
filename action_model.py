import torch
from pytorchvideo.models.hub import slowfast_r50

model = slowfast_r50(pretrained=True)
model.eval()

def predict_action(frames):

    video = torch.tensor(frames).permute(3,0,1,2).float()
    video = video / 255.0
    video = video.unsqueeze(0)

    fast_pathway = video

    slow_pathway = torch.index_select(
        video,
        2,
        torch.linspace(0, video.shape[2]-1, video.shape[2]//4).long()
    )

    inputs = [slow_pathway, fast_pathway]

    with torch.no_grad():
        pred = model(inputs)

    return pred