class Linked_list_node:

	def __init__(self,submission):
		self.sub = submission
		self.p = None
		self.n = None

	def getSubmission():
		return self.sub

class submissionListAndMap:

	def __init__(self):
		self.head = None
		self.tail = None
		self.map = {}
		self.size = 0


	def insert(self,submission):

		if submission == None:
			return -1 #Error should not happen

		new_node = Linked_list_node(submission)

		self.insertSubmissionNode(new_node)
		# self.map[submission.getLearnerId()] = new_node

		# if self.head == None:
		# 	self.head = new_node
		# 	self.tail = new_node
		# else:
		# 	self.tail.n = new_node
		# 	self.tail = new_node

		# self.size =self.size + 1

	def remove(self,learnerId):

		if learnerId not in self.map:
			return -1 # Should not happen

		submisisonNode = self.map[learnerId]


		prevNode = submission.p
		nextNode = submission.n

		if prevNode != None:
			prevNode.n = nextNode
		if nextNode != None:
			nextNode.p = prevNode

		if self.head == submisisonNode:
			self.head = nextNode

		if self.tail == submisisonNode:
			self.tail = prevNode

		self.size =self.size - 1

		del self.map[learnerId]

	def insertSubmissionNode(self,subNode):

		self.map[subNode.getSubmission().getLearnerId()] = subNode

		if self.head == None:
			self.head = subNode
			self.tail = subNode
		else:
			self.tail.n = subNode
			self.tail = subNode

		self.size =self.size + 1

	def appendOtherListandMap(self,other):

		if other.size == 0:
			return

		temp = other.head

		while temp is not None:

			temp.sub.setState(SubmissionState.ReadyToReview)
			self.insertSubmissionNode(temp)
			temp = temp.n






class SubmissionPool:

	def __init__(self):
		self.subLM = submissionListAndMap()  #Submitted
		self.revLM = submissionListAndMap()   # Ready to review or being reviewed
		self.reviewedLM = submissionListAndMap() # Graded


	def addsubmission(self,submission):
		self.subLM.insert(submission)

	def removeSubmission(self,submission):

		submitterid = submission.getLearnerId()

		self.subLM.remove(submitterid)


	def markSubmissionsReadyToReview(self):

		self.revLM.appendOtherListandMap(self.subLM)

		self.subLM = submissionListAndMap()


	def addReviewerForSubmission(self,submisison,reviewerId):

		if reviewerId not in self.ReviewerSubmissionMap:
			self.ReviewerSubmissionMap[reviewerId] = []

		self.ReviewerSubmissionMap[reviewerId].append(submisison.getLearnerId())

		submission.addReviwer()

	def getSubmissionToReview(self,learnerId):

		subId = -1
		minSubTime = sys.maxint
		minLearnerId = sys.maxint

		for idx in xrange(len(self.submissions)):
			sub = self.submissions[idx]
			subLid = sub.getLearnerId()
			if subLid == learnerId :
				continue

			if learnerId in self.ReviewerSubmissionMap and subLid in self.ReviewerSubmissionMap[learnerId]:
				continue

			subState = sub.getState()

			if subState != SubmissionState.ReadyToReview and submisison != SubmissionState.BeingReviewedReviewersNeeded:
				continue

			subTime = sub.getSubmissionTime()
			if (subTime < minSubTime) or ((subTime == minSubTime) and (subLid < minLearnerId)):
				subId = idx
				minSubTime = subTime
				minLearnerId = subLid
				continue
			
		if subId == -1:
			return None

		retval = self.submissions[subId]

		return retval





