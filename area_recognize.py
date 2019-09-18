import tensorflow as tf
import numpy as np
import pandas as pd
import cv2
import os
import time

class AreaRecognize(object):
	"""docstring for AreaRecognize"""
	def __init__(self, top_k=1):
		self.top_k = top_k
		self.image_graph_dir = "model/classify_image_graph_def.pb"
		self.human_label_map_dir = "model/imagenet_synset_to_human_label_map.txt"
		self.challenge_label_map_dir = "model/imagenet_2012_challenge_label_map_proto.pbtxt"
		self.rec_result = pd.DataFrame(np.zeros((1, 2)), columns=['label', 'score'])
		self.make_id_name_dic()
		self.create_graph()

	def make_id_name_dic(self):
		uid_to_human = {}
		for line in tf.gfile.GFile(self.human_label_map_dir).readlines():
			items = line.strip().split('\t')
			uid_to_human[items[0]] = items[1]

		node_id_to_uid = {}
		for line in tf.gfile.GFile(self.challenge_label_map_dir).readlines():
			if line.startswith('  target_class:'):
				target_class = int(line.split(': ')[1])
			if line.startswith('  target_class_string:'):
				target_class_string = line.split(': ')[1].strip('\n').strip('\"')
				node_id_to_uid[target_class] = target_class_string
				
		self.node_id_to_name = {}
		for key, value in node_id_to_uid.items():
			self.node_id_to_name[key] = uid_to_human[value]	



	def create_graph(self):
		with tf.gfile.FastGFile(self.image_graph_dir, 'rb') as f:
			graph_def = tf.GraphDef()
			graph_def.ParseFromString(f.read())
			_ = tf.import_graph_def(graph_def, name='')


	def recognize(self, image_dir, sess):
		self.image_data = tf.gfile.FastGFile(image_dir, 'rb').read()
		# with tf.Session() as sess:
			# 'softmax:0': A tensor containing the normalized prediction across 1000 labels
			# 'pool_3:0': A tensor containing the next-to-last layer containing 2048 float description of the image
			# 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG encoding of the image
		softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
		predictions = sess.run(softmax_tensor, feed_dict={'DecodeJpeg/contents:0': self.image_data})
		predictions = np.squeeze(predictions)

		top_k = predictions.argsort()[-self.top_k:]
		self.rec_num = len(top_k)
		self.rec_result = pd.DataFrame(np.zeros((self.rec_num, 2)), columns=['label', 'score'])
		count = 0
		for node_id in top_k:
			label = self.node_id_to_name[node_id]
			score = predictions[node_id]
			print('%s (score = %.5f)' % (label, score))
			self.rec_result.iloc[count,0], self.rec_result.iloc[count,1] = label, score
			count += 1 


if __name__ == '__main__':
	test_folder = "img_data/world"
	file_list = os.listdir(test_folder)

	area_recognize = AreaRecognize()
	with tf.Session() as sess:
		for files in file_list:
			img_dir = os.path.join(test_folder, files)
			t1 = time.time()
			area_recognize.recognize(img_dir, sess)
			print(area_recognize.rec_result.iloc[-1, 0])
			t2 = time.time()
			print("计算耗时：", t2-t1)
			if cv2.waitKey(1) == 27:
			    break
			else:
			    pass