{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/gist/15-30219-2/0c3d40d033054c4da6bcbdef19b60e0b/untitled0.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 108
        },
        "id": "2XNzX5o6oHuK",
        "outputId": "f2e5e1ad-75eb-49f5-c412-8dda0e15b945"
      },
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<IPython.core.display.HTML object>"
            ],
            "text/html": [
              "\n",
              "     <input type=\"file\" id=\"files-f2e41bc4-57e0-4290-bd4b-f89ba8550f39\" name=\"files[]\" multiple disabled\n",
              "        style=\"border:none\" />\n",
              "     <output id=\"result-f2e41bc4-57e0-4290-bd4b-f89ba8550f39\">\n",
              "      Upload widget is only available when the cell has been executed in the\n",
              "      current browser session. Please rerun this cell to enable.\n",
              "      </output>\n",
              "      <script>// Copyright 2017 Google LLC\n",
              "//\n",
              "// Licensed under the Apache License, Version 2.0 (the \"License\");\n",
              "// you may not use this file except in compliance with the License.\n",
              "// You may obtain a copy of the License at\n",
              "//\n",
              "//      http://www.apache.org/licenses/LICENSE-2.0\n",
              "//\n",
              "// Unless required by applicable law or agreed to in writing, software\n",
              "// distributed under the License is distributed on an \"AS IS\" BASIS,\n",
              "// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n",
              "// See the License for the specific language governing permissions and\n",
              "// limitations under the License.\n",
              "\n",
              "/**\n",
              " * @fileoverview Helpers for google.colab Python module.\n",
              " */\n",
              "(function(scope) {\n",
              "function span(text, styleAttributes = {}) {\n",
              "  const element = document.createElement('span');\n",
              "  element.textContent = text;\n",
              "  for (const key of Object.keys(styleAttributes)) {\n",
              "    element.style[key] = styleAttributes[key];\n",
              "  }\n",
              "  return element;\n",
              "}\n",
              "\n",
              "// Max number of bytes which will be uploaded at a time.\n",
              "const MAX_PAYLOAD_SIZE = 100 * 1024;\n",
              "\n",
              "function _uploadFiles(inputId, outputId) {\n",
              "  const steps = uploadFilesStep(inputId, outputId);\n",
              "  const outputElement = document.getElementById(outputId);\n",
              "  // Cache steps on the outputElement to make it available for the next call\n",
              "  // to uploadFilesContinue from Python.\n",
              "  outputElement.steps = steps;\n",
              "\n",
              "  return _uploadFilesContinue(outputId);\n",
              "}\n",
              "\n",
              "// This is roughly an async generator (not supported in the browser yet),\n",
              "// where there are multiple asynchronous steps and the Python side is going\n",
              "// to poll for completion of each step.\n",
              "// This uses a Promise to block the python side on completion of each step,\n",
              "// then passes the result of the previous step as the input to the next step.\n",
              "function _uploadFilesContinue(outputId) {\n",
              "  const outputElement = document.getElementById(outputId);\n",
              "  const steps = outputElement.steps;\n",
              "\n",
              "  const next = steps.next(outputElement.lastPromiseValue);\n",
              "  return Promise.resolve(next.value.promise).then((value) => {\n",
              "    // Cache the last promise value to make it available to the next\n",
              "    // step of the generator.\n",
              "    outputElement.lastPromiseValue = value;\n",
              "    return next.value.response;\n",
              "  });\n",
              "}\n",
              "\n",
              "/**\n",
              " * Generator function which is called between each async step of the upload\n",
              " * process.\n",
              " * @param {string} inputId Element ID of the input file picker element.\n",
              " * @param {string} outputId Element ID of the output display.\n",
              " * @return {!Iterable<!Object>} Iterable of next steps.\n",
              " */\n",
              "function* uploadFilesStep(inputId, outputId) {\n",
              "  const inputElement = document.getElementById(inputId);\n",
              "  inputElement.disabled = false;\n",
              "\n",
              "  const outputElement = document.getElementById(outputId);\n",
              "  outputElement.innerHTML = '';\n",
              "\n",
              "  const pickedPromise = new Promise((resolve) => {\n",
              "    inputElement.addEventListener('change', (e) => {\n",
              "      resolve(e.target.files);\n",
              "    });\n",
              "  });\n",
              "\n",
              "  const cancel = document.createElement('button');\n",
              "  inputElement.parentElement.appendChild(cancel);\n",
              "  cancel.textContent = 'Cancel upload';\n",
              "  const cancelPromise = new Promise((resolve) => {\n",
              "    cancel.onclick = () => {\n",
              "      resolve(null);\n",
              "    };\n",
              "  });\n",
              "\n",
              "  // Wait for the user to pick the files.\n",
              "  const files = yield {\n",
              "    promise: Promise.race([pickedPromise, cancelPromise]),\n",
              "    response: {\n",
              "      action: 'starting',\n",
              "    }\n",
              "  };\n",
              "\n",
              "  cancel.remove();\n",
              "\n",
              "  // Disable the input element since further picks are not allowed.\n",
              "  inputElement.disabled = true;\n",
              "\n",
              "  if (!files) {\n",
              "    return {\n",
              "      response: {\n",
              "        action: 'complete',\n",
              "      }\n",
              "    };\n",
              "  }\n",
              "\n",
              "  for (const file of files) {\n",
              "    const li = document.createElement('li');\n",
              "    li.append(span(file.name, {fontWeight: 'bold'}));\n",
              "    li.append(span(\n",
              "        `(${file.type || 'n/a'}) - ${file.size} bytes, ` +\n",
              "        `last modified: ${\n",
              "            file.lastModifiedDate ? file.lastModifiedDate.toLocaleDateString() :\n",
              "                                    'n/a'} - `));\n",
              "    const percent = span('0% done');\n",
              "    li.appendChild(percent);\n",
              "\n",
              "    outputElement.appendChild(li);\n",
              "\n",
              "    const fileDataPromise = new Promise((resolve) => {\n",
              "      const reader = new FileReader();\n",
              "      reader.onload = (e) => {\n",
              "        resolve(e.target.result);\n",
              "      };\n",
              "      reader.readAsArrayBuffer(file);\n",
              "    });\n",
              "    // Wait for the data to be ready.\n",
              "    let fileData = yield {\n",
              "      promise: fileDataPromise,\n",
              "      response: {\n",
              "        action: 'continue',\n",
              "      }\n",
              "    };\n",
              "\n",
              "    // Use a chunked sending to avoid message size limits. See b/62115660.\n",
              "    let position = 0;\n",
              "    do {\n",
              "      const length = Math.min(fileData.byteLength - position, MAX_PAYLOAD_SIZE);\n",
              "      const chunk = new Uint8Array(fileData, position, length);\n",
              "      position += length;\n",
              "\n",
              "      const base64 = btoa(String.fromCharCode.apply(null, chunk));\n",
              "      yield {\n",
              "        response: {\n",
              "          action: 'append',\n",
              "          file: file.name,\n",
              "          data: base64,\n",
              "        },\n",
              "      };\n",
              "\n",
              "      let percentDone = fileData.byteLength === 0 ?\n",
              "          100 :\n",
              "          Math.round((position / fileData.byteLength) * 100);\n",
              "      percent.textContent = `${percentDone}% done`;\n",
              "\n",
              "    } while (position < fileData.byteLength);\n",
              "  }\n",
              "\n",
              "  // All done.\n",
              "  yield {\n",
              "    response: {\n",
              "      action: 'complete',\n",
              "    }\n",
              "  };\n",
              "}\n",
              "\n",
              "scope.google = scope.google || {};\n",
              "scope.google.colab = scope.google.colab || {};\n",
              "scope.google.colab._files = {\n",
              "  _uploadFiles,\n",
              "  _uploadFilesContinue,\n",
              "};\n",
              "})(self);\n",
              "</script> "
            ]
          },
          "metadata": {}
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Saving kaggle (2).json to kaggle (2).json\n",
            "User uploaded file \"kaggle (2).json\" with length 65 bytes\n",
            "mv: cannot stat 'kaggle.json': No such file or directory\n"
          ]
        }
      ],
      "source": [
        "from google.colab import files\n",
        "\n",
        "uploaded = files.upload()\n",
        "\n",
        "for fn in uploaded.keys():\n",
        "  print('User uploaded file \"{name}\" with length {length} bytes'.format(\n",
        "      name=fn, length=len(uploaded[fn])))\n",
        "\n",
        "# Then move kaggle.json into the folder where the API expects to find it.\n",
        "!mkdir -p ~/.kaggle/ && mv kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "_KvAd67ixxPA",
        "outputId": "c7d10dfb-d49d-47ed-a7e6-a7bb00cd3bab"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Dataset URL: https://www.kaggle.com/datasets/kabil007/lungcancer4types-imagedataset\n",
            "License(s): apache-2.0\n",
            "Downloading lungcancer4types-imagedataset.zip to /content\n",
            " 89% 105M/119M [00:01<00:00, 106MB/s]  \n",
            "100% 119M/119M [00:01<00:00, 91.9MB/s]\n"
          ]
        }
      ],
      "source": [
        "!kaggle datasets download -d kabil007/lungcancer4types-imagedataset"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Za5F30gi9FNg",
        "outputId": "f12f84b5-492b-4708-abaa-e675bcbb0689"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Done\n"
          ]
        }
      ],
      "source": [
        "from zipfile import ZipFile\n",
        "file_name = \"/content/lungcancer4types-imagedataset.zip\"\n",
        "with ZipFile(file_name,'r') as zip:\n",
        "  zip.extractall()\n",
        "  print('Done')\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "qg7jzkwbyZIy"
      },
      "outputs": [],
      "source": [
        "import numpy as np\n",
        "from sklearn import preprocessing\n",
        "from sklearn.model_selection import train_test_split\n",
        "from keras.models import Sequential\n",
        "from keras.layers import Convolution2D, Dropout, Dense,MaxPooling2D\n",
        "from keras.layers import BatchNormalization\n",
        "from keras.layers import MaxPooling2D\n",
        "from keras.layers import Flatten"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Cxa-fpehxZpN",
        "outputId": "40447959-669d-4e82-cf50-ee5d29be35a6"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            " 16%|█▌        | 19/120 [00:00<00:00, 179.49it/s]"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            " 45%|████▌     | 54/120 [00:00<00:00, 157.18it/s]"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            " 75%|███████▌  | 90/120 [00:00<00:00, 169.03it/s]"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "100%|██████████| 120/120 [00:00<00:00, 169.27it/s]\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n",
            "adenocarcinoma\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            " 43%|████▎     | 22/51 [00:00<00:00, 212.14it/s]"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "\r 88%|████████▊ | 45/51 [00:00<00:00, 221.51it/s]"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "\r100%|██████████| 51/51 [00:00<00:00, 218.25it/s]\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n",
            "large.cell.carcinoma\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "\r  0%|          | 0/54 [00:00<?, ?it/s]"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "\r 19%|█▊        | 10/54 [00:00<00:00, 95.40it/s]"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "\r 39%|███▉      | 21/54 [00:00<00:00, 100.66it/s]"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "\r 59%|█████▉    | 32/54 [00:00<00:00, 92.88it/s] "
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "\r 78%|███████▊  | 42/54 [00:00<00:00, 79.14it/s]"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "100%|██████████| 54/54 [00:00<00:00, 87.29it/s]\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "normal\n",
            "normal\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "\r  0%|          | 0/90 [00:00<?, ?it/s]"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "\r 18%|█▊        | 16/90 [00:00<00:00, 158.99it/s]"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "\r 36%|███▌      | 32/90 [00:00<00:00, 158.57it/s]"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "\r 56%|█████▌    | 50/90 [00:00<00:00, 168.28it/s]"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "\r 79%|███████▉  | 71/90 [00:00<00:00, 183.80it/s]"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "\r100%|██████████| 90/90 [00:00<00:00, 180.97it/s]\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "squamous.cell.carcinoma\n",
            "squamous.cell.carcinoma\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "100%|██████████| 195/195 [00:00<00:00, 241.04it/s]\n",
            "100%|██████████| 115/115 [00:00<00:00, 256.50it/s]\n",
            "100%|██████████| 148/148 [00:01<00:00, 113.24it/s]\n",
            "100%|██████████| 155/155 [00:00<00:00, 234.95it/s]\n",
            "100%|██████████| 23/23 [00:00<00:00, 238.13it/s]\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n",
            "adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "100%|██████████| 21/21 [00:00<00:00, 248.72it/s]\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n",
            "large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "\r  0%|          | 0/13 [00:00<?, ?it/s]"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "100%|██████████| 13/13 [00:00<00:00, 67.17it/s]\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n",
            "normal\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "\r  0%|          | 0/15 [00:00<?, ?it/s]"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa\n",
            "squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "\r100%|██████████| 15/15 [00:00<00:00, 237.71it/s]"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa\n",
            "squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa\n",
            "squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa\n",
            "squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa\n",
            "squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa\n",
            "squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa\n",
            "squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa\n",
            "squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa\n",
            "squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa\n",
            "squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa\n",
            "squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa\n",
            "squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa\n",
            "squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa\n",
            "['adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'adenocarcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'large.cell.carcinoma', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'squamous.cell.carcinoma', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa']\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "\n"
          ]
        }
      ],
      "source": [
        "import os\n",
        "import cv2\n",
        "from tqdm import tqdm\n",
        "\n",
        "# Initialize the lists for images and labels\n",
        "X = []\n",
        "y = []\n",
        "\n",
        "# Define the full paths for the subfolders\n",
        "base_test_dir = '/content/Data/test'\n",
        "base_train_dir = '/content/Data/train'\n",
        "base_valid_dir = '/content/Data/valid'\n",
        "\n",
        "# Process test data\n",
        "test_folders = ['adenocarcinoma', 'large.cell.carcinoma', 'normal', 'squamous.cell.carcinoma']\n",
        "\n",
        "for folder in test_folders:\n",
        "    folder_path = os.path.join(base_test_dir, folder)  # Full path to the subfolder\n",
        "    if not os.path.exists(folder_path):\n",
        "        print(f\"Warning: {folder_path} not found.\")\n",
        "        continue\n",
        "\n",
        "    for i in tqdm(os.listdir(folder_path)):\n",
        "        # Check if the file is an image\n",
        "        if not any(i.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']):\n",
        "            continue  # Skip non-image files\n",
        "        img_path = os.path.join(folder_path, i)  # Full path to the image file\n",
        "        img = cv2.imread(img_path)\n",
        "        if img is None:\n",
        "            print(f\"Error loading image: {img_path}\")\n",
        "            continue  # Skip if the image is not loaded properly\n",
        "\n",
        "        img = cv2.resize(img, (224, 224))  # Resize to 224x224\n",
        "        X.append(img)\n",
        "        y.append(folder)  # Use the folder name as the label\n",
        "        print(folder)\n",
        "\n",
        "# Process train data\n",
        "train_folders = ['adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'normal', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa']\n",
        "\n",
        "for folder in train_folders:\n",
        "    folder_path = os.path.join(base_train_dir, folder)  # Full path to the subfolder\n",
        "    if not os.path.exists(folder_path):\n",
        "        print(f\"Warning: {folder_path} not found.\")\n",
        "        continue\n",
        "\n",
        "    for i in tqdm(os.listdir(folder_path)):\n",
        "        # Check if the file is an image\n",
        "        if not any(i.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']):\n",
        "            continue  # Skip non-image files\n",
        "        img_path = os.path.join(folder_path, i)  # Full path to the image file\n",
        "        img = cv2.imread(img_path)\n",
        "        if img is None:\n",
        "            print(f\"Error loading image: {img_path}\")\n",
        "            continue  # Skip if the image is not loaded properly\n",
        "\n",
        "        img = cv2.resize(img, (224, 224))  # Resize to 224x224\n",
        "        X.append(img)\n",
        "        y.append('N')  # Assuming 'N' for all training data (you can adjust as needed)\n",
        "\n",
        "# Process validation data\n",
        "valid_folders = ['adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 'normal', 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa']\n",
        "\n",
        "for folder in valid_folders:\n",
        "    folder_path = os.path.join(base_valid_dir, folder)  # Full path to the subfolder\n",
        "    if not os.path.exists(folder_path):\n",
        "        print(f\"Warning: {folder_path} not found.\")\n",
        "        continue\n",
        "\n",
        "    for i in tqdm(os.listdir(folder_path)):\n",
        "        # Check if the file is an image\n",
        "        if not any(i.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']):\n",
        "            continue  # Skip non-image files\n",
        "        img_path = os.path.join(folder_path, i)  # Full path to the image file\n",
        "        img = cv2.imread(img_path)\n",
        "        if img is None:\n",
        "            print(f\"Error loading image: {img_path}\")\n",
        "            continue  # Skip if the image is not loaded properly\n",
        "\n",
        "        img = cv2.resize(img, (224, 224))  # Resize to 224x224\n",
        "        X.append(img)\n",
        "        y.append(folder)  # Use the folder name as the label\n",
        "        print(folder)\n",
        "\n",
        "# Optionally, print the labels to check\n",
        "print(y)\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 205
        },
        "id": "od82i1-R4p3g",
        "outputId": "9862a0d7-d950-410c-84ad-8d18ec5c1216"
      },
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 1000x1000 with 4 Axes>"
            ],
            "image/png": "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\n"
          },
          "metadata": {}
        }
      ],
      "source": [
        "%matplotlib inline\n",
        "import matplotlib.pyplot as plt\n",
        "plt.figure(figsize=(10, 10))\n",
        "for i in range(4):\n",
        "    plt.subplot(1, 4, i+1)\n",
        "    plt.imshow(X[i], cmap=\"gray\")\n",
        "    plt.axis('off')\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "GndgC7784-Po",
        "outputId": "74479c1e-ebfc-486b-b131-9c790b0c32ac"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Shape of an image in X_train:  (224, 224, 3)\n",
            "Shape of an image in X_test:  (224, 224, 3)\n"
          ]
        }
      ],
      "source": [
        "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)\n",
        "print (\"Shape of an image in X_train: \", X_train[0].shape)\n",
        "print (\"Shape of an image in X_test: \", X_test[0].shape)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "O0g6vrZR5hV6",
        "outputId": "8a40d21c-1cf7-4c69-b660-0fcaf0427b12"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "y_train type: <class 'list'>, shape: (670,)\n",
            "y_test type: <class 'list'>, shape: (330,)\n",
            "y_train_encoded: [0 6 0 0 1 0 0 0 0 0 0 0 5 3 0 0 0 0 1 2 5 6 0 1 6 3 6 0 0 3 0 0 3 0 3 1 0\n",
            " 5 0 0 3 0 3 5 1 0 0 1 0 0 6 3 0 6 5 0 0 3 7 0 5 1 0 1 0 1 0 0 0 7 1 0 0 0\n",
            " 0 0 0 0 1 0 0 0 0 6 0 0 0 0 0 0 1 0 0 0 0 0 1 1 0 6 6 0 0 0 6 1 5 0 0 0 5\n",
            " 0 4 0 0 0 0 5 0 0 0 0 0 3 6 0 0 0 0 0 1 1 0 4 0 1 1 0 0 0 0 1 2 1 0 7 0 2\n",
            " 0 0 0 1 1 0 0 1 1 0 3 0 0 0 0 1 0 5 0 0 0 0 0 5 0 0 0 4 0 0 4 0 6 0 0 1 0\n",
            " 0 5 5 5 1 0 0 0 0 0 0 0 5 0 1 0 1 0 6 0 0 3 1 0 0 5 6 6 0 1 2 0 0 0 3 1 0\n",
            " 0 1 0 0 0 6 1 0 5 7 0 0 6 0 0 6 0 4 3 3 0 1 0 0 3 0 0 0 0 1 0 0 0 0 0 0 1\n",
            " 5 6 0 0 0 0 3 6 0 0 0 1 3 0 6 0 4 5 1 0 0 5 6 0 0 0 0 5 0 5 1 0 3 0 5 1 0\n",
            " 1 4 2 0 4 0 6 0 0 6 1 4 0 4 0 6 1 4 0 0 4 0 0 0 5 0 0 0 4 0 0 4 3 0 3 0 7\n",
            " 0 1 6 0 1 0 0 0 0 0 0 1 1 3 0 2 5 0 0 0 1 0 1 0 0 6 6 0 0 0 0 0 6 0 6 0 3\n",
            " 0 0 0 0 0 0 3 3 0 2 0 0 0 0 0 5 3 0 0 3 4 5 0 6 6 0 3 5 5 0 6 0 2 0 0 0 0\n",
            " 3 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 5 0 6 0 0 0 1 0 6 0 0 0 0 5 0 6 0 0 0 0\n",
            " 0 0 0 0 6 0 0 0 6 0 0 5 4 0 0 0 0 0 7 2 0 0 0 0 0 0 0 4 0 0 1 6 0 3 0 1 0\n",
            " 3 0 0 0 0 2 0 1 0 6 0 0 0 0 0 0 5 0 0 0 0 0 5 1 0 0 2 0 0 0 0 0 1 0 0 0 0\n",
            " 0 1 1 0 0 5 3 1 0 6 0 0 0 6 0 0 0 0 0 3 1 0 0 3 5 0 0 4 1 0 1 3 1 0 0 5 0\n",
            " 5 0 1 0 0 0 0 0 6 0 6 0 0 0 7 0 0 6 5 3 0 0 0 0 0 0 0 1 0 0 1 2 5 0 1 5 1\n",
            " 0 0 0 0 0 1 0 0 0 0 0 6 1 0 0 0 6 3 0 7 0 0 0 5 0 0 6 0 0 0 0 5 0 0 0 0 0\n",
            " 1 0 0 0 0 6 1 6 0 3 6 4 5 0 0 0 0 0 0 6 0 3 0 0 1 0 1 0 0 5 0 3 0 1 0 1 1\n",
            " 6 0 0 1], shape: (670,)\n",
            "y_test_encoded: [0 0 0 0 0 0 0 0 0 3 0 1 0 5 2 0 6 0 0 0 0 5 0 0 5 6 1 7 0 2 0 3 0 0 0 5 0\n",
            " 0 0 1 0 1 6 5 6 6 0 0 0 0 0 0 6 0 1 1 0 1 5 0 6 1 0 5 0 0 0 0 1 0 1 0 0 0\n",
            " 6 6 0 1 0 6 0 1 6 1 0 0 7 0 0 0 0 0 0 5 0 0 0 1 1 0 0 0 2 6 0 0 0 4 3 0 0\n",
            " 0 7 0 1 0 5 5 0 6 0 0 0 6 6 0 0 0 0 0 0 0 6 7 0 1 3 5 1 1 1 6 0 6 0 0 0 6\n",
            " 0 0 0 3 5 0 2 0 6 0 1 0 0 0 0 0 0 0 6 0 6 6 0 0 1 7 0 0 6 6 0 0 0 0 0 0 0\n",
            " 3 0 0 2 0 2 0 0 5 5 0 0 5 0 1 1 0 0 0 0 0 3 0 0 0 1 3 0 0 0 0 0 6 0 0 6 0\n",
            " 5 1 0 1 0 0 0 0 0 7 0 0 1 1 6 4 5 0 1 5 0 0 6 1 0 1 1 6 1 7 0 0 0 0 0 0 0\n",
            " 1 0 0 1 6 0 0 0 0 0 0 0 1 0 6 0 1 5 0 1 0 0 0 6 6 5 0 0 0 6 2 2 0 0 0 0 0\n",
            " 2 0 1 3 0 0 0 0 0 2 0 0 2 0 0 0 0 0 0 0 6 0 0 5 1 3 6 0 0 0 0 0 0 3], shape: (330,)\n",
            "Number of classes: 8\n",
            "X_train shape: (670, 224, 224, 3)\n",
            "y_train shape: (670, 8)\n",
            "X_test shape: (330, 224, 224, 3)\n",
            "y_test shape: (330, 8)\n"
          ]
        }
      ],
      "source": [
        "from sklearn import preprocessing\n",
        "import numpy as np\n",
        "import tensorflow as tf\n",
        "\n",
        "# Ensure y_train and y_test are defined and in the correct format\n",
        "# For example, ensure they are lists or NumPy arrays of labels (not one-hot encoded yet)\n",
        "\n",
        "# Check the type and shape of y_train and y_test\n",
        "print(f\"y_train type: {type(y_train)}, shape: {np.shape(y_train)}\")\n",
        "print(f\"y_test type: {type(y_test)}, shape: {np.shape(y_test)}\")\n",
        "\n",
        "# Initialize the LabelEncoder\n",
        "le = preprocessing.LabelEncoder()\n",
        "\n",
        "# Fit and transform y_train\n",
        "y_train_encoded = le.fit_transform(y_train)  # Converts labels to integers\n",
        "print(f\"y_train_encoded: {y_train_encoded}, shape: {y_train_encoded.shape}\")\n",
        "\n",
        "# Transform y_test using the same encoder\n",
        "y_test_encoded = le.transform(y_test)  # Converts labels to integers\n",
        "print(f\"y_test_encoded: {y_test_encoded}, shape: {y_test_encoded.shape}\")\n",
        "\n",
        "# Dynamically determine the number of classes for one-hot encoding\n",
        "num_classes = len(np.unique(y_train_encoded))\n",
        "print(f\"Number of classes: {num_classes}\")\n",
        "\n",
        "# Convert to one-hot encoding\n",
        "y_train_categorical = tf.keras.utils.to_categorical(y_train_encoded, num_classes=num_classes)\n",
        "y_test_categorical = tf.keras.utils.to_categorical(y_test_encoded, num_classes=num_classes)\n",
        "\n",
        "# Convert all data to NumPy arrays\n",
        "y_train = np.array(y_train_categorical)\n",
        "y_test = np.array(y_test_categorical)\n",
        "X_train = np.array(X_train)\n",
        "X_test = np.array(X_test)\n",
        "\n",
        "# Final checks\n",
        "print(f\"X_train shape: {X_train.shape}\")\n",
        "print(f\"y_train shape: {y_train.shape}\")\n",
        "print(f\"X_test shape: {X_test.shape}\")\n",
        "print(f\"y_test shape: {y_test.shape}\")\n",
        "\n"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "print(\"X_train Shape: \", X_train.shape)\n",
        "print(\"X_test Shape: \", X_test.shape)\n",
        "print(\"y_train Shape: \", y_train.shape)\n",
        "print(\"y_test Shape: \", y_test.shape)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "-DRC1-Xjd8YJ",
        "outputId": "b50c6fa7-ae78-47e9-ad9c-1618eb507d48"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "X_train Shape:  (670, 224, 224, 3)\n",
            "X_test Shape:  (330, 224, 224, 3)\n",
            "y_train Shape:  (670, 8)\n",
            "y_test Shape:  (330, 8)\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from keras.applications import vgg16\n",
        "\n",
        "\n",
        "img_rows, img_cols = 224, 224\n",
        "\n",
        "\n",
        "vgg = vgg16.VGG16(weights = 'imagenet',\n",
        "                 include_top = False,\n",
        "                 input_shape = (img_rows, img_cols, 3))\n",
        "\n",
        "# Here we freeze the last 4 layers\n",
        "# Layers are set to trainable as True by default\n",
        "for layer in vgg.layers:\n",
        "    layer.trainable = False\n",
        "\n",
        "# Let's print our layers\n",
        "for (i,layer) in enumerate(vgg.layers):\n",
        "    print(str(i) + \" \"+ layer.__class__.__name__, layer.trainable)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "cthlFMgvf4o-",
        "outputId": "070cfdaf-94db-402b-ffb4-e8948235e97d"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "0 InputLayer False\n",
            "1 Conv2D False\n",
            "2 Conv2D False\n",
            "3 MaxPooling2D False\n",
            "4 Conv2D False\n",
            "5 Conv2D False\n",
            "6 MaxPooling2D False\n",
            "7 Conv2D False\n",
            "8 Conv2D False\n",
            "9 Conv2D False\n",
            "10 MaxPooling2D False\n",
            "11 Conv2D False\n",
            "12 Conv2D False\n",
            "13 Conv2D False\n",
            "14 MaxPooling2D False\n",
            "15 Conv2D False\n",
            "16 Conv2D False\n",
            "17 Conv2D False\n",
            "18 MaxPooling2D False\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        " def lw(bottom_model, num_classes):\n",
        "    \"\"\"creates the top or head of the model that will be\n",
        "    placed ontop of the bottom layers\"\"\"\n",
        "\n",
        "    top_model = bottom_model.output\n",
        "    top_model = GlobalAveragePooling2D()(top_model)\n",
        "    top_model = Dense(1024,activation='relu')(top_model)\n",
        "    top_model = Dense(1024,activation='relu')(top_model)\n",
        "    top_model = Dense(512,activation='relu')(top_model)\n",
        "    top_model = Dense(num_classes,activation='softmax')(top_model)\n",
        "    return top_model"
      ],
      "metadata": {
        "id": "uJqfTnRghLWD"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        " from keras.models import Sequential\n",
        "from keras.layers import Dense, Dropout, Activation, Flatten, GlobalAveragePooling2D\n",
        "from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D\n",
        "\n",
        "from keras.models import Model\n",
        "\n",
        "\n",
        "num_classes = 2\n",
        "\n",
        "FC_Head = lw(vgg, num_classes)\n",
        "\n",
        "model = Model(inputs = vgg.input, outputs = FC_Head)\n",
        "\n",
        "print(model.summary())"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 930
        },
        "id": "3a5Z1Q9lhq3u",
        "outputId": "0a1bb273-3765-4227-e2c8-a35b5eecfbe2"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "\u001b[1mModel: \"functional_25\"\u001b[0m\n"
            ],
            "text/html": [
              "<pre style=\"white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\"><span style=\"font-weight: bold\">Model: \"functional_25\"</span>\n",
              "</pre>\n"
            ]
          },
          "metadata": {}
        },
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓\n",
              "┃\u001b[1m \u001b[0m\u001b[1mLayer (type)                        \u001b[0m\u001b[1m \u001b[0m┃\u001b[1m \u001b[0m\u001b[1mOutput Shape               \u001b[0m\u001b[1m \u001b[0m┃\u001b[1m \u001b[0m\u001b[1m        Param #\u001b[0m\u001b[1m \u001b[0m┃\n",
              "┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩\n",
              "│ input_layer_13 (\u001b[38;5;33mInputLayer\u001b[0m)          │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m224\u001b[0m, \u001b[38;5;34m224\u001b[0m, \u001b[38;5;34m3\u001b[0m)         │               \u001b[38;5;34m0\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block1_conv1 (\u001b[38;5;33mConv2D\u001b[0m)                │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m224\u001b[0m, \u001b[38;5;34m224\u001b[0m, \u001b[38;5;34m64\u001b[0m)        │           \u001b[38;5;34m1,792\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block1_conv2 (\u001b[38;5;33mConv2D\u001b[0m)                │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m224\u001b[0m, \u001b[38;5;34m224\u001b[0m, \u001b[38;5;34m64\u001b[0m)        │          \u001b[38;5;34m36,928\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block1_pool (\u001b[38;5;33mMaxPooling2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m112\u001b[0m, \u001b[38;5;34m112\u001b[0m, \u001b[38;5;34m64\u001b[0m)        │               \u001b[38;5;34m0\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block2_conv1 (\u001b[38;5;33mConv2D\u001b[0m)                │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m112\u001b[0m, \u001b[38;5;34m112\u001b[0m, \u001b[38;5;34m128\u001b[0m)       │          \u001b[38;5;34m73,856\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block2_conv2 (\u001b[38;5;33mConv2D\u001b[0m)                │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m112\u001b[0m, \u001b[38;5;34m112\u001b[0m, \u001b[38;5;34m128\u001b[0m)       │         \u001b[38;5;34m147,584\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block2_pool (\u001b[38;5;33mMaxPooling2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m56\u001b[0m, \u001b[38;5;34m56\u001b[0m, \u001b[38;5;34m128\u001b[0m)         │               \u001b[38;5;34m0\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block3_conv1 (\u001b[38;5;33mConv2D\u001b[0m)                │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m56\u001b[0m, \u001b[38;5;34m56\u001b[0m, \u001b[38;5;34m256\u001b[0m)         │         \u001b[38;5;34m295,168\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block3_conv2 (\u001b[38;5;33mConv2D\u001b[0m)                │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m56\u001b[0m, \u001b[38;5;34m56\u001b[0m, \u001b[38;5;34m256\u001b[0m)         │         \u001b[38;5;34m590,080\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block3_conv3 (\u001b[38;5;33mConv2D\u001b[0m)                │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m56\u001b[0m, \u001b[38;5;34m56\u001b[0m, \u001b[38;5;34m256\u001b[0m)         │         \u001b[38;5;34m590,080\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block3_pool (\u001b[38;5;33mMaxPooling2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m28\u001b[0m, \u001b[38;5;34m28\u001b[0m, \u001b[38;5;34m256\u001b[0m)         │               \u001b[38;5;34m0\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block4_conv1 (\u001b[38;5;33mConv2D\u001b[0m)                │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m28\u001b[0m, \u001b[38;5;34m28\u001b[0m, \u001b[38;5;34m512\u001b[0m)         │       \u001b[38;5;34m1,180,160\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block4_conv2 (\u001b[38;5;33mConv2D\u001b[0m)                │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m28\u001b[0m, \u001b[38;5;34m28\u001b[0m, \u001b[38;5;34m512\u001b[0m)         │       \u001b[38;5;34m2,359,808\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block4_conv3 (\u001b[38;5;33mConv2D\u001b[0m)                │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m28\u001b[0m, \u001b[38;5;34m28\u001b[0m, \u001b[38;5;34m512\u001b[0m)         │       \u001b[38;5;34m2,359,808\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block4_pool (\u001b[38;5;33mMaxPooling2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m14\u001b[0m, \u001b[38;5;34m14\u001b[0m, \u001b[38;5;34m512\u001b[0m)         │               \u001b[38;5;34m0\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block5_conv1 (\u001b[38;5;33mConv2D\u001b[0m)                │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m14\u001b[0m, \u001b[38;5;34m14\u001b[0m, \u001b[38;5;34m512\u001b[0m)         │       \u001b[38;5;34m2,359,808\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block5_conv2 (\u001b[38;5;33mConv2D\u001b[0m)                │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m14\u001b[0m, \u001b[38;5;34m14\u001b[0m, \u001b[38;5;34m512\u001b[0m)         │       \u001b[38;5;34m2,359,808\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block5_conv3 (\u001b[38;5;33mConv2D\u001b[0m)                │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m14\u001b[0m, \u001b[38;5;34m14\u001b[0m, \u001b[38;5;34m512\u001b[0m)         │       \u001b[38;5;34m2,359,808\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block5_pool (\u001b[38;5;33mMaxPooling2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m7\u001b[0m, \u001b[38;5;34m7\u001b[0m, \u001b[38;5;34m512\u001b[0m)           │               \u001b[38;5;34m0\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ global_average_pooling2d_5           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m512\u001b[0m)                 │               \u001b[38;5;34m0\u001b[0m │\n",
              "│ (\u001b[38;5;33mGlobalAveragePooling2D\u001b[0m)             │                             │                 │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ dense_36 (\u001b[38;5;33mDense\u001b[0m)                     │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m1024\u001b[0m)                │         \u001b[38;5;34m525,312\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ dense_37 (\u001b[38;5;33mDense\u001b[0m)                     │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m1024\u001b[0m)                │       \u001b[38;5;34m1,049,600\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ dense_38 (\u001b[38;5;33mDense\u001b[0m)                     │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m512\u001b[0m)                 │         \u001b[38;5;34m524,800\u001b[0m │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ dense_39 (\u001b[38;5;33mDense\u001b[0m)                     │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m2\u001b[0m)                   │           \u001b[38;5;34m1,026\u001b[0m │\n",
              "└──────────────────────────────────────┴─────────────────────────────┴─────────────────┘\n"
            ],
            "text/html": [
              "<pre style=\"white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\">┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓\n",
              "┃<span style=\"font-weight: bold\"> Layer (type)                         </span>┃<span style=\"font-weight: bold\"> Output Shape                </span>┃<span style=\"font-weight: bold\">         Param # </span>┃\n",
              "┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩\n",
              "│ input_layer_13 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">InputLayer</span>)          │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">224</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">224</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">3</span>)         │               <span style=\"color: #00af00; text-decoration-color: #00af00\">0</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block1_conv1 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)                │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">224</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">224</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">64</span>)        │           <span style=\"color: #00af00; text-decoration-color: #00af00\">1,792</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block1_conv2 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)                │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">224</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">224</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">64</span>)        │          <span style=\"color: #00af00; text-decoration-color: #00af00\">36,928</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block1_pool (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">MaxPooling2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">112</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">112</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">64</span>)        │               <span style=\"color: #00af00; text-decoration-color: #00af00\">0</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block2_conv1 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)                │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">112</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">112</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">128</span>)       │          <span style=\"color: #00af00; text-decoration-color: #00af00\">73,856</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block2_conv2 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)                │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">112</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">112</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">128</span>)       │         <span style=\"color: #00af00; text-decoration-color: #00af00\">147,584</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block2_pool (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">MaxPooling2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">56</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">56</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">128</span>)         │               <span style=\"color: #00af00; text-decoration-color: #00af00\">0</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block3_conv1 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)                │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">56</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">56</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">256</span>)         │         <span style=\"color: #00af00; text-decoration-color: #00af00\">295,168</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block3_conv2 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)                │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">56</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">56</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">256</span>)         │         <span style=\"color: #00af00; text-decoration-color: #00af00\">590,080</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block3_conv3 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)                │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">56</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">56</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">256</span>)         │         <span style=\"color: #00af00; text-decoration-color: #00af00\">590,080</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block3_pool (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">MaxPooling2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">28</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">28</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">256</span>)         │               <span style=\"color: #00af00; text-decoration-color: #00af00\">0</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block4_conv1 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)                │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">28</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">28</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)         │       <span style=\"color: #00af00; text-decoration-color: #00af00\">1,180,160</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block4_conv2 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)                │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">28</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">28</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)         │       <span style=\"color: #00af00; text-decoration-color: #00af00\">2,359,808</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block4_conv3 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)                │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">28</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">28</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)         │       <span style=\"color: #00af00; text-decoration-color: #00af00\">2,359,808</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block4_pool (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">MaxPooling2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">14</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">14</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)         │               <span style=\"color: #00af00; text-decoration-color: #00af00\">0</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block5_conv1 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)                │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">14</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">14</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)         │       <span style=\"color: #00af00; text-decoration-color: #00af00\">2,359,808</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block5_conv2 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)                │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">14</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">14</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)         │       <span style=\"color: #00af00; text-decoration-color: #00af00\">2,359,808</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block5_conv3 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)                │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">14</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">14</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)         │       <span style=\"color: #00af00; text-decoration-color: #00af00\">2,359,808</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ block5_pool (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">MaxPooling2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">7</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">7</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)           │               <span style=\"color: #00af00; text-decoration-color: #00af00\">0</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ global_average_pooling2d_5           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)                 │               <span style=\"color: #00af00; text-decoration-color: #00af00\">0</span> │\n",
              "│ (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">GlobalAveragePooling2D</span>)             │                             │                 │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ dense_36 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Dense</span>)                     │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">1024</span>)                │         <span style=\"color: #00af00; text-decoration-color: #00af00\">525,312</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ dense_37 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Dense</span>)                     │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">1024</span>)                │       <span style=\"color: #00af00; text-decoration-color: #00af00\">1,049,600</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ dense_38 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Dense</span>)                     │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)                 │         <span style=\"color: #00af00; text-decoration-color: #00af00\">524,800</span> │\n",
              "├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤\n",
              "│ dense_39 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Dense</span>)                     │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">2</span>)                   │           <span style=\"color: #00af00; text-decoration-color: #00af00\">1,026</span> │\n",
              "└──────────────────────────────────────┴─────────────────────────────┴─────────────────┘\n",
              "</pre>\n"
            ]
          },
          "metadata": {}
        },
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "\u001b[1m Total params: \u001b[0m\u001b[38;5;34m16,815,426\u001b[0m (64.15 MB)\n"
            ],
            "text/html": [
              "<pre style=\"white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\"><span style=\"font-weight: bold\"> Total params: </span><span style=\"color: #00af00; text-decoration-color: #00af00\">16,815,426</span> (64.15 MB)\n",
              "</pre>\n"
            ]
          },
          "metadata": {}
        },
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "\u001b[1m Trainable params: \u001b[0m\u001b[38;5;34m2,100,738\u001b[0m (8.01 MB)\n"
            ],
            "text/html": [
              "<pre style=\"white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\"><span style=\"font-weight: bold\"> Trainable params: </span><span style=\"color: #00af00; text-decoration-color: #00af00\">2,100,738</span> (8.01 MB)\n",
              "</pre>\n"
            ]
          },
          "metadata": {}
        },
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "\u001b[1m Non-trainable params: \u001b[0m\u001b[38;5;34m14,714,688\u001b[0m (56.13 MB)\n"
            ],
            "text/html": [
              "<pre style=\"white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\"><span style=\"font-weight: bold\"> Non-trainable params: </span><span style=\"color: #00af00; text-decoration-color: #00af00\">14,714,688</span> (56.13 MB)\n",
              "</pre>\n"
            ]
          },
          "metadata": {}
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "None\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from tensorflow.keras.models import Model\n",
        "model.compile(optimizer='adam', loss = 'categorical_crossentropy',metrics = ['accuracy'])"
      ],
      "metadata": {
        "id": "cnpYb87-jLvy"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "from sklearn import preprocessing\n",
        "import numpy as np\n",
        "import tensorflow as tf\n",
        "\n",
        "# Assume X_train, X_test, y_train, y_test are preloaded\n",
        "\n",
        "# Ensure y_train and y_test are 1D for encoding\n",
        "if len(y_train.shape) > 1:\n",
        "    y_train = np.argmax(y_train, axis=1)\n",
        "if len(y_test.shape) > 1:\n",
        "    y_test = np.argmax(y_test, axis=1)\n",
        "\n",
        "# Encode labels\n",
        "le = preprocessing.LabelEncoder()\n",
        "y_train_encoded = le.fit_transform(y_train)\n",
        "y_test_encoded = le.transform(y_test)\n",
        "\n",
        "# One-hot encode labels\n",
        "num_classes = len(np.unique(y_train_encoded))\n",
        "y_train_categorical = tf.keras.utils.to_categorical(y_train_encoded, num_classes=num_classes)\n",
        "y_test_categorical = tf.keras.utils.to_categorical(y_test_encoded, num_classes=num_classes)\n",
        "\n",
        "# Normalize input data\n",
        "X_train = X_train.astype('float32') / 255.0\n",
        "X_test = X_test.astype('float32') / 255.0\n",
        "\n",
        "# Define the model\n",
        "model = tf.keras.Sequential([\n",
        "    tf.keras.layers.Input(shape=(224, 224, 3)),\n",
        "    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),\n",
        "    tf.keras.layers.MaxPooling2D((2, 2)),\n",
        "    tf.keras.layers.Flatten(),\n",
        "    tf.keras.layers.Dense(64, activation='relu'),\n",
        "    tf.keras.layers.Dense(num_classes, activation='softmax')\n",
        "])\n",
        "\n",
        "# Compile the model\n",
        "model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])\n",
        "\n",
        "# Train the model\n",
        "history = model.fit(\n",
        "    X_train, y_train_categorical,\n",
        "    epochs=5,\n",
        "    validation_data=(X_test, y_test_categorical),\n",
        "    verbose=1,\n",
        "    initial_epoch=0\n",
        ")\n",
        "\n",
        "# Print history\n",
        "print(history.history)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "scIza-LRjTlg",
        "outputId": "ec695d3d-9e1f-486f-ac7d-48b4d0784507"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Epoch 1/5\n",
            "\u001b[1m21/21\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m39s\u001b[0m 2s/step - accuracy: 0.5333 - loss: 9.8832 - val_accuracy: 0.6818 - val_loss: 2.1495\n",
            "Epoch 2/5\n",
            "\u001b[1m21/21\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m38s\u001b[0m 2s/step - accuracy: 0.6963 - loss: 1.2793 - val_accuracy: 0.7394 - val_loss: 0.9199\n",
            "Epoch 3/5\n",
            "\u001b[1m21/21\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m42s\u001b[0m 2s/step - accuracy: 0.7586 - loss: 0.7088 - val_accuracy: 0.7667 - val_loss: 0.8383\n",
            "Epoch 4/5\n",
            "\u001b[1m21/21\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m47s\u001b[0m 2s/step - accuracy: 0.8058 - loss: 0.5324 - val_accuracy: 0.7727 - val_loss: 0.8861\n",
            "Epoch 5/5\n",
            "\u001b[1m21/21\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m77s\u001b[0m 2s/step - accuracy: 0.8739 - loss: 0.3677 - val_accuracy: 0.7788 - val_loss: 0.8320\n",
            "{'accuracy': [0.5686567425727844, 0.720895528793335, 0.7820895314216614, 0.825373113155365, 0.8716418147087097], 'loss': [6.997845649719238, 1.0822513103485107, 0.6353883743286133, 0.4705106019973755, 0.33868634700775146], 'val_accuracy': [0.6818181872367859, 0.739393949508667, 0.7666666507720947, 0.7727272510528564, 0.7787878513336182], 'val_loss': [2.1494686603546143, 0.919897198677063, 0.8383136987686157, 0.8861213326454163, 0.8320472240447998]}\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import matplotlib.pyplot as plt\n",
        "%matplotlib inline\n",
        "acc = history.history['accuracy']\n",
        "val_acc = history.history['val_accuracy']\n",
        "loss = history.history['loss']\n",
        "val_loss = history.history['val_loss']\n",
        "\n",
        "epochs = range(len(acc))\n",
        "\n",
        "plt.plot(epochs, acc, 'r', label='Training accuracy')\n",
        "plt.plot(epochs, val_acc, 'b', label='Validation accuracy')\n",
        "plt.title('Training and validation accuracy')\n",
        "plt.legend(loc=0)\n",
        "plt.figure()\n",
        "\n",
        "plt.show()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 469
        },
        "id": "MHDKE4Z-_5FB",
        "outputId": "fd5df12a-70e4-47d3-f274-51fdd8f5766c"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 640x480 with 1 Axes>"
            ],
            "image/png": "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\n"
          },
          "metadata": {}
        },
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 640x480 with 0 Axes>"
            ]
          },
          "metadata": {}
        }
      ]
    }
  ],
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPr3tS0dpKURhBpNxQhsOkG",
      "include_colab_link": true
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}