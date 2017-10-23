# -*- coding: utf-8 -*-
# /usr/bin/python2

from __future__ import print_function

from data_load import *
from models import Model
import argparse
from hyperparams import logdir_path


def eval(logdir='logdir/default/train2', queue=True):
    # Load graph
    model = Model(mode="test2", batch_size=hp.test2.batch_size, queue=queue)

    # Loss
    loss_op = model.loss_net2()

    # Summary
    summ_op = summaries(loss_op)

    session_conf = tf.ConfigProto(
        allow_soft_placement=True,
        device_count={'CPU': 1, 'GPU': 0},
    )
    with tf.Session(config=session_conf) as sess:
        # Load trained model
        sess.run(tf.global_variables_initializer())
        model.load(sess, 'test2', logdir=logdir)

        writer = tf.summary.FileWriter(logdir, sess.graph)

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)

        if queue:
            summ, loss = sess.run([summ_op, loss_op])
        else:
            x, y = get_batch(model.mode, model.batch_size)
            summ, loss = sess.run([summ_op, loss_op], feed_dict={model.x_mfcc: x, model.y_spec: y})

        writer.add_summary(summ)
        writer.close()

        coord.request_stop()
        coord.join(threads)

        print("loss:", loss)


def summaries(loss):
    tf.summary.scalar('net2/eval/loss', loss)
    return tf.summary.merge_all()


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('case', type=str, help='case')
    arguments = parser.parse_args()
    return arguments


if __name__ == '__main__':
    args = get_arguments()
    case = args.case
    logdir = '{}/{}/train2'.format(logdir_path, case)
    eval(logdir=logdir)
    print("Done")
