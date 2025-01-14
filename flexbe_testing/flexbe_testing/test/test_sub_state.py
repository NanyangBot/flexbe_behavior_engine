#!/usr/bin/env python
import rclpy
from flexbe_core import EventState
from flexbe_core.proxy import ProxySubscriberCached

from std_msgs.msg import String

class TestSubState(EventState):

	def __init__(self, topic):
		'''Constructor'''
		super(TestSubState, self).__init__(outcomes=['received', 'unavailable'],
										output_keys=['output_value'])
		self._topic = topic
		self._sub = ProxySubscriberCached({self._topic: String}, id=id(self))
		self._msg_counter = 0
		self._timeout = TestSubState._node.get_clock().now() + rclpy.duration.Duration(seconds=1.5)


	def execute(self, userdata):
		if self._msg_counter == 0 and TestSubState._node.get_clock().now() > self._timeout:
			userdata.output_value = None
			return 'unavailable'

		if self._sub.has_msg(self._topic):
			msg = self._sub.get_last_msg(self._topic)
			self._sub.remove_last_msg(self._topic)
			userdata.output_value = msg.data
			self._msg_counter += 1

		if self._msg_counter == 3:
			return 'received'
