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
		self.current = -1


	def __iter__(self):
        return self

    def next(self):
		retval = None 
		if self.current == -1:
			if self.head == None:
				raise StopIteration
			self.current = self.head.n
			retval = self.head
		elif self.current == None:
			raise StopIteration
		else:
			retval = self.current
			self.current = self.current.n
		return retval.getSubmission()


	def insert(self,submission):

		if submission == None:
			return -1 #Error should not happen

		new_node = Linked_list_node(submission)

		self.insertNode(new_node)

	def remove(self,learnerId):

		if learnerId not in self.map:
			return -1 # Should not happen

		submisisonNode = self.map[learnerId]

		self.removeNode(submisisonNode)

	def removeNode(self,node):

		prevNode = node.p
		nextNode = node.n

		if prevNode != None:
			prevNode.n = nextNode
		if nextNode != None:
			nextNode.p = prevNode

		if self.head == node:
			self.head = nextNode

		if self.tail == node:
			self.tail = prevNode

		self.size =self.size - 1

		lId = node.getSubmission().getLearnerId()

		del self.map[lId]



	def insertNode(self,subNode):

		self.map[subNode.getSubmission().getLearnerId()] = subNode

		if self.head == None:
			self.head = subNode
			self.tail = subNode
		else:
			self.tail.n = subNode
			self.tail = subNode

		self.size =self.size + 1

	def appendOtherListandMap(self,other):

		#TODO optimize this 
		if other.size == 0:
			return

		temp = other.head

		while temp is not None:

			temp.sub.setState(SubmissionState.ReadyToReview)
			self.insertNode(temp)
			temp = temp.n

	def appendOtherListNodeInaParticularState(self,other,state):

		if other.size == 0:
			return 

		temp = other.head

		while temp is not None:

			if temp.getSubmission().getState() == state:

				self.insertNode(temp)

				prev = temp
				temp = temp.n

				other.removeNode(prev)








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

	def removeFailedSubmission(self,submitterid):

		self.reviewedLM.remove(submitterid)



	def markSubmissionsReadyToReview(self):

		self.revLM.appendOtherListandMap(self.subLM)

		self.subLM = submissionListAndMap()

	def markGradedSubmissions(self):

		self.reviewedLM.appendOtherListNodeInaParticularState(self.revLM,SubmissionState.GradeReady)



	def getSubmissionToReview(self,learnerId,submissionsAlreadyReviewed):

		minsub = None
		minSubTime = sys.maxint
		minLearnerId = sys.maxint

		for sub in self.revLM:
			subLid = sub.getLearnerId()
			if subLid == learnerId :
				continue

			if subLid in submissionsAlreadyReviewed:
				continue

			# if learnerId in self.ReviewerSubmissionMap and subLid in self.ReviewerSubmissionMap[learnerId]:
			# 	continue

			subState = sub.getState()

			if subState != SubmissionState.ReadyToReview and submisison != SubmissionState.BeingReviewedReviewersNeeded:
				continue

			subTime = sub.getSubmissionTime()
			if (subTime < minSubTime) or ((subTime == minSubTime) and (subLid < minLearnerId)):
				minsub = sub
				minSubTime = subTime
				minLearnerId = subLid
				continue
			
		if minsub == None:
			return None

		minsub.addReviwer(learnerId)

		return minsub





