import gradio as gr
import pandas as pd
from all_models import models

data = pd.read_csv("video_data.csv")

# 获取ID列表、模型名称列表，并构建视频路径字典
ids = data["ID"].unique()
# models = data.columns[5:]  # 从第5列开始为模型名称列
video_paths = {
    row["ID"]: {model: row[model] for model in models}
    for _, row in data.iterrows()
}
num_models = 14
default_models = models[:6]

# 定义函数：加载指定ID的Text Prompt
def load_prompt(id):
    row = data[data["ID"] == id].iloc[0]
    return row["Text Prompt"]


# 定义函数：根据选择的模型动态生成视频框布局
def extend_choices(choices):
    print(f"Extending choices: {choices}")
    extended = choices[:num_models] + (num_models - len(choices[:num_models])) * ['Null']
    print(f"Extended choices: {extended}")
    return extended
def update_videos(id,choices):
    print(f"Updating image boxes with choices: {choices}")
    choices_plus = extend_choices(choices[:num_models])
    vidboxes = []
    for m in choices_plus:
        if m != 'Null':
            video_path = video_paths[id][m]
            if video_path and not pd.isna(video_path):
                vidboxes.append(gr.Video(video_path, label=m, visible=True))
            elif pd.isna(video_path):
                vidboxes.append(gr.Video(label=m, visible=True))
            else:
                vidboxes.append(gr.Video(label=m, visible=False))
        else:
            vidboxes.append(gr.Video(visible=False))  # 无效模型隐藏

    print(f"Updated video boxes: {vidboxes}")
    return vidboxes

# 定义函数：同步播放所有视频
def sync_play(*videos):
    # 返回每个视频的播放进度重置到0
    return [(video, 0) if video else None for video in videos]


# 创建Gradio界面
with gr.Blocks() as demo:
    gr.HTML("<center><h1>模型视频生成效果比较工具</h1></center>")

    # ID选择和Prompt显示
    with gr.Row():
        id_selector = gr.Dropdown(label="选择ID", choices=ids.tolist(), interactive=True)
        prompt_display = gr.Textbox(label="Applied Prompt", interactive=False)

    # 使用Accordion包装模型选择框
    with gr.Accordion('Model Selection'):
        # 模型选择器
        model_selector = gr.CheckboxGroup(models, label=f"从以下{len(models)}个模型中选择以进行比较", value=default_models, interactive=True)

    with gr.Row():
        # Create image output components for each model
        output = [gr.Video(label=m, min_width=320) for m in models]
        # Create hidden textboxes to store the current models
        current_models = [gr.Textbox(m, visible=False) for m in models]

    # 更新Prompt和视频播放区内容
    id_selector.change(fn=load_prompt, inputs=id_selector, outputs=prompt_display)
    # id_selector.change(fn=update_videos, inputs=[id_selector, model_selector], outputs=output)  # 传递 id_selector 作为输入
    model_selector.change(fn=update_videos, inputs=[id_selector, model_selector], outputs=output)  # 传递 id_selector 作为输入
    model_selector.change(fn=extend_choices, inputs=model_selector, outputs=current_models)
    # 同步播放按钮
    sync_button = gr.Button("同步播放视频")
    sync_button.click(fn=sync_play, inputs=output, outputs=output)
    # sync_button.click(fn=sync_play, inputs=video_display_area, outputs=video_display_area)

demo.launch(allowed_paths=["/mnt/jfs-hdd/sora/samples/VideoGenEval-complete/VideoGen-Eval1.0/separate"])