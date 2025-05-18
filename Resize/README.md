## Resize

### resize_pair.py

Resize your hq/lq image pair created for training a SISR model to a max width of 1920 and/or a max heigh of 1080.

Written to work with image pair created by [WTP Dataset Destroyer](https://github.com/umzi2/wtp_dataset_destroyer) but should work with any.
Change input and output dir as well as desired max dimensions.

### resize_single.py

Resize your HQ image dataset to a max width of 1920 and/or a max heigh of 1080.

Written for prepping the dataset to give to [WTP Dataset Destroyer](https://github.com/umzi2/wtp_dataset_destroyer) so that it works with a dataset at max dimensions of your choosing for perhaps faster training later on.
Change input and output dir as well as desired max dimensions.

