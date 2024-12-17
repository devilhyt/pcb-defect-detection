#!/bin/bash
mkdir -p datasets
cd datasets

curl -L -o pcb-defect-dataset.zip\
  https://www.kaggle.com/api/v1/datasets/download/norbertelter/pcb-defect-dataset

unzip pcb-defect-dataset.zip