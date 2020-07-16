import json
import os
from datetime import datetime
from keras import backend as kb


def custom_log(model, others={}, save_model=True, log_file="logs"):
    now = datetime.now()
    now_str = now.strftime("%Y_%m_%d__%H_%M_%S")
    if save_model:
        model.save("saved_models/" + now_str + ".h5")

    params = model.history.params
    history = model.history.history
    results = {
        "acc": [round(x, 4) for x in history['acc']],
        "val_acc": [round(x, 4) for x in history['val_acc']],
        "loss": [round(x, 4) for x in history['loss']],
        "val_loss": [round(x, 4) for x in history['val_loss']]
    }

    layers = []
    for ly in model.get_config()["layers"]:
        layers.append({
            "name": "" if "name" not in ly["config"] else ly["config"]["name"],
            "units": "" if "units" not in ly["config"] else ly["config"]["units"],
            "use_bias": "" if "use_bias" not in ly["config"] else ly["config"]["use_bias"],
            "activation": "" if "activation" not in ly["config"] else ly["config"]["activation"],
            "trainable": "" if "trainable" not in ly["config"] else ly["config"]["trainable"],
        })
    log = {
        "date": now_str,
        "history": results,
        "input_shape": model.input_shape,
        "layers": layers,
        "params": params,
        "params_count": f"{model.count_params():,d}",
        "loss": model.loss,
        "optimizer": {
            "type": type(model.optimizer).__name__,
            "lr": str(kb.eval(model.optimizer.lr))
        },
        "others": others
    }

    filename = 'analyse/' + log_file + '.json'
    if os.path.exists(filename):
        append_write = 'r+'
    else:
        append_write = 'w+'

    with open(filename, append_write) as jsn:
        f = jsn.read()
        json_obj = []
        if f is not '':
            json_obj = json.loads(f)
            jsn.seek(0)

        json_obj.append(log)
        jsn.write(json.dumps(json_obj))
        jsn.truncate()
