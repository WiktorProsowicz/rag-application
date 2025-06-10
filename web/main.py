import gradio as gr

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)


    
if __name__ == "__main__":
    with gr.Interface(fn=greet,
                        inputs=["text", "slider"],outputs=["text"]) as demo:
        demo.title = "Greeting App"