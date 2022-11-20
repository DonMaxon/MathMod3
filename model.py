from queue import Queue
import numpy as np
from random import random, randint
from math import log


class Task:

	def __init__(self, time):
		self.time = time


class Line:

	def __init__(self, id, status):
		self.id = id
		self.status = status
		self.free = True

	def get_curr_params(self):
		return self.free if self.status else self.status

	def put(self, task):
		if self.free:
			self.time = task.time
			self.free = False
			return True
		return False

	def upd_free(self):
		if not self.free:
			self.time -= 1
			if self.time <= 0:
				self.free = True


class SMOQueue:

	def __init__(self, cap):
		self.cap = cap
		self.q = Queue()
		self.len = 0

	def put(self, task):
		if self.q.qsize() == self.cap:
			return False
		else:
			self.q.put(task)
			self.len += 1
			return True

	def get_out(self):
		if not self.q.empty():
			self.len -= 1
			return self.q.get()
		else:
			return False


class SMO:

	def __init__(self, mod_time, start_lines, max_lines, time_coeff, dur_coeff, cap):
		self.q = SMOQueue(cap=cap)
		self.dur_coeff = dur_coeff
		self.max_lines = max_lines
		self.lines_active = start_lines
		self.lines = np.array([])
		for i in range(max_lines):
			if i < start_lines:
				self.lines = np.append(self.lines, [Line(i + 1, True)])
			else:
				self.lines = np.append(self.lines, [Line(i + 1, False)])
		self.mod_time = mod_time
		self.current_time = 0
		self.times = np.array([-np.log(random())/time_coeff])
		while True:
			self.times = np.append(self.times, [-np.log(random())/time_coeff + self.times[-1]])
			if self.times[-1] > self.mod_time:
				self.times = self.times[:-1]
				break
		self.tasks_num = 0
		self.accepted = 0
		self.rejected = 0

	def step(self):
		count = self.times[self.times < self.current_time].shape[0]
		if count != 0:
			self.tasks_num += count
			if self.q.len != 0:
				for i in range(self.q.len):
					task = self.q.get_out()
					put = False
					if task:
						for j in range(self.max_lines):
							if self.lines[j].status and self.lines[j].put(task):
								put = True
								break
						if put:
							self.accepted += 1
			for i in range(count):
				task = Task(-log(random())/self.dur_coeff)
				put = False
				for j in range(self.max_lines):
					if self.lines[j].status and self.lines[j].put(task):
						put = True
						break
				if put:
					self.accepted += 1
				elif not self.q.put(task):
					if self.lines_active < self.max_lines:
						for k in range(self.max_lines):
							if not self.lines[k].status:
								self.lines[k].status = True
								self.lines[k].put(task)
								self.lines_active += 1
					else:
						self.rejected += 1
		for line in self.lines:
			line.upd_free()
		self.current_time += 1
		if self.q.len == 0 and self.lines_active > 1:
			indexes = []
			for line in self.lines:
				if line.free and line.status:
					indexes.append(line.id - 1)
			if len(indexes) > 0:
				self.lines[indexes[randint(0, len(indexes) - 1)]].status = False
				self.lines_active -= 1
		self.times = self.times[count:]
		return self.lines, self.q, self.tasks_num, self.accepted, self.rejected