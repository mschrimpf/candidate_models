import pytest
from pytest import approx

from brainscore.benchmarks.imagenet import Imagenet2012
from candidate_models import brain_translated_pool
from tests.flags import requires_gpu, memory_intense


@memory_intense
@requires_gpu
class TestImagenet:
    @pytest.mark.parametrize(['model', 'expected_top1'], [
        # pytorch: from https://pytorch.org/docs/stable/torchvision/models.html
        ('alexnet', 1 - .4345),
        ('squeezenet1_0', 1 - .4190),
        ('squeezenet1_1', 1 - .4181),
        ('resnet-18', 1 - .3024),
        ('resnet-34', 1 - .2670),
        # keras: from https://keras.io/applications/#documentation-for-individual-models
        ('xception', .790),
        ('vgg-16', .713),
        ('vgg-19', .713),
        ('densenet-121', .750),
        ('densenet-169', .762),
        ('densenet-201', .773),
        # tf-slim: from
        # https://github.com/tensorflow/models/tree/b3158fb0183809400e9e7f8092dd541201b1c4d4/research/slim#pre-trained-models
        ('inception_v1', .698),
        ('inception_v2', .739),
        ('inception_v3', .780),
        ('inception_v4', .802),
        ('inception_resnet_v2', .804),
        ('resnet-50_v1', .752),
        ('resnet-101_v1', .764),
        ('resnet-152_v1', .768),
        ('resnet-50_v2', .756),
        ('resnet-101_v2', .770),
        ('resnet-152_v2', .778),
        ('nasnet_mobile', .740),
        ('nasnet_large', .827),
        ('pnasnet_large', .829),
        ('mobilenet_v1_1.0_224', 0.709),
        ('mobilenet_v1_1.0_192', 0.7),
        ('mobilenet_v1_1.0_160', 0.68),
        ('mobilenet_v1_1.0_128', 0.652),
        ('mobilenet_v1_0.75_224', 0.684),
        ('mobilenet_v1_0.75_192', 0.672),
        ('mobilenet_v1_0.75_160', 0.653),
        ('mobilenet_v1_0.75_128', 0.621),
        ('mobilenet_v1_0.5_224', 0.633),
        ('mobilenet_v1_0.5_192', 0.617),
        ('mobilenet_v1_0.5_160', 0.591),
        ('mobilenet_v1_0.5_128', 0.563),
        ('mobilenet_v1_0.25_224', 0.498),
        ('mobilenet_v1_0.25_192', 0.477),
        ('mobilenet_v1_0.25_160', 0.455),
        ('mobilenet_v1_0.25_128', 0.415),
        ('mobilenet_v2_1.4_224', 0.75),
        ('mobilenet_v2_1.3_224', 0.744),
        ('mobilenet_v2_1.0_224', 0.718),
        ('mobilenet_v2_1.0_192', 0.707),
        ('mobilenet_v2_1.0_160', 0.688),
        ('mobilenet_v2_1.0_128', 0.653),
        ('mobilenet_v2_1.0_96', 0.603),
        ('mobilenet_v2_0.75_224', 0.698),
        ('mobilenet_v2_0.75_192', 0.687),
        ('mobilenet_v2_0.75_160', 0.664),
        ('mobilenet_v2_0.75_128', 0.632),
        ('mobilenet_v2_0.75_96', 0.588),
        ('mobilenet_v2_0.5_224', 0.654),
        ('mobilenet_v2_0.5_192', 0.639),
        ('mobilenet_v2_0.5_160', 0.61),
        ('mobilenet_v2_0.5_128', 0.577),
        ('mobilenet_v2_0.5_96', 0.512),
        ('mobilenet_v2_0.35_224', 0.603),
        ('mobilenet_v2_0.35_192', 0.582),
        ('mobilenet_v2_0.35_160', 0.557),
        ('mobilenet_v2_0.35_128', 0.508),
        ('mobilenet_v2_0.35_96', 0.455),
        # bagnet: own runs
        ('bagnet9', .2635),
        ('bagnet17', .46),
        ('bagnet33', .58924),
    ])
    def test_top1(self, model, expected_top1):
        import tensorflow as tf
        tf.reset_default_graph()
        import keras
        keras.backend.clear_session()
        _model = brain_translated_pool[model]
        benchmark = Imagenet2012()
        score = benchmark(_model)
        accuracy = score.sel(aggregation='center')
        assert accuracy == approx(expected_top1, abs=.07)
