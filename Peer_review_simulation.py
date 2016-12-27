import sys


class SubmissionState:
	Start,WorkedOn,Submitted ,ReadyToReview ,BeingReviewedReviewersNeeded,BeingReviewedNoMoreReviwersNeeded,GradeReady = range(7)


class Submission:

	def __init__(self,submissionTime,learnerId, trueScore):

		self.state = SubmissionState.Start
		self.submissionTime = submissionTime
		self.learnerId = learnerId
		self.grade = 0
		self.numReviewers = 0
		self.reviewsCompleted = 0
		self.trueScore = trueScore
		self.reviewers = []
		self.gradeTick = -1

	def getTrueScore(self):
		return self.trueScore

	def getLearnerId(self):
		return self.learnerId

	def getSubmissionTime(self):
		return self.submissionTime


	def getState(self):
		return self.state

	def setState(self,state):
		self.state = state

	def getGrade(self):
		return self.grade

	def getGradeTick(self):
		return self.gradeTick


	def addGrade(self,grade,current_tick):

		if self.state != SubmissionState.BeingReviewedReviewersNeeded\
		and self.state != SubmissionState.BeingReviewedNoMoreReviwersNeeded:
			return -1 #Should not happen

		self.reviewsCompleted = self.reviewsCompleted + 1

		if self.grade == -1:
			self.grade = grade
		else:
			self.grade = self.grade + grade

		if self.reviewsCompleted == 3:
			self.state = SubmissionState.GradeReady
			self.gradeTick = current_tick

	def getGradeIfReady(self):

		if self.state == SubmissionState.GradeReady:
			return self.grade

		return -1

	def isPassingGrade(self):

		if self.state != SubmissionState.GradeReady:
			return -1

		if self.grade >= 240:
			return 1

		return 0

	def getReviewers(self):
		return self.reviewers

	def addReviewer(self,reviewerId):

		if self.state != SubmissionState.ReadyToReview and self.state != SubmissionState.BeingReviewedReviewersNeeded:
			return -1  #Should not happen

		if self.state == SubmissionState.ReadyToReview:
			self.reviewers.append(reviewerId)
			self.numReviewers = 1
			self.state = SubmissionState.BeingReviewedReviewersNeeded
		elif self.state == SubmissionState.BeingReviewedReviewersNeeded:
			self.reviewers.append(reviewerId)
			self.numReviewers = self.numReviewers + 1
			if self.reviewsCompleted + self.numReviewers == 3:
				self.state = SubmissionState.BeingReviewedNoMoreReviwersNeeded







class SubmissionNode:

	def __init__(self,submission):
		self.sub = submission
		self.p = None
		self.n = None

	def getSubmission(self):
		return self.sub

class submissionListAndMap:

	def __init__(self):
		self.head = None
		self.tail = None
		self.map = {}
		self.size = 0
		self.current = -1

	def getSize(self):
		return self.size

	def __iter__(self):
		self.current = -1
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

		new_node = SubmissionNode(submission)

		self.insertNode(new_node)

	def remove(self,learnerId):

		if learnerId not in self.map:
			return -1 # Should not happen

		submisisonNode = self.map[learnerId]

		self.removeNode(submisisonNode)

	def removeNode(self,node):


		if self.size == 1:
			self.head = None
			self.tail = None
			self.size = 0
		else:
			prevNode = node.p
			nextNode = node.n

			if prevNode != None:
				prevNode.n = nextNode
			if nextNode != None:
				nextNode.p = prevNode

			if self.head == node and prevNode != None:
				self.head = prevNode
			elif self.head == node:
				self.head = nextNode

			if self.tail == node and nextNode != None:
				self.tail = nextNode
			elif self.tail == node:
				self.tail = prevNode

			self.size =self.size - 1

		lId = node.getSubmission().getLearnerId()

		del self.map[lId]



	def insertNode(self,subNode):

		self.map[subNode.getSubmission().getLearnerId()] = subNode

		if self.head == None and self.tail == None:
			self.head = subNode
			self.tail = subNode
		else:
			self.tail.n = subNode
			subNode.p = self.tail
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
			else:
				temp = temp.n





class SubmissionPool:

	def __init__(self):
		self.subLM = submissionListAndMap()  #Submitted
		self.revLM = submissionListAndMap()   # Ready to review or being reviewed

	def addSubmissionToPool(self,submission):
		self.subLM.insert(submission)

	def removeSubmission(self,submission):

		submitterid = submission.getLearnerId()

		self.subLM.remove(submitterid)

	def removeFailedSubmission(self,submitterid):

		self.revLM.remove(submitterid)

	def markSubmissionsReadyToReview(self):

		if self.subLM.getSize() > 0:

			self.revLM.appendOtherListandMap(self.subLM)

			self.subLM = submissionListAndMap()


	def getSubmissionToReviewAndAddReviewer(self,learnerId,submissionsAlreadyReviewed):

		minsub = None
		minSubTime = sys.maxint
		minLearnerId = sys.maxint

		print "Debug 0 getSubmissionToReviewAndAddReviewer " + str(learnerId) + "size of review pool " + str(self.revLM.getSize())
		for sub in self.revLM:
			subLid = sub.getLearnerId()

			print "Debug 1 getSubmissionToReviewAndAddReviewer " + str(learnerId) + " Sublid " + str(subLid)
			if subLid == learnerId :
				continue

			print "Debug 2 getSubmissionToReviewAndAddReviewer " + str(learnerId) + " Sublid " + str(subLid)
			if subLid in submissionsAlreadyReviewed:
				continue

			print "Debug 3 getSubmissionToReviewAndAddReviewer " + str(learnerId) + " Sublid " + str(subLid)

			subState = sub.getState()

			if subState != SubmissionState.ReadyToReview and subState != SubmissionState.BeingReviewedReviewersNeeded:
				continue

			print "Debug 4 getSubmissionToReviewAndAddReviewer " + str(learnerId) + " Sublid " + str(subLid)
			subTime = sub.getSubmissionTime()
			if (subTime < minSubTime) or ((subTime == minSubTime) and (subLid < minLearnerId)):
				print "Debug 5 getSubmissionToReviewAndAddReviewer " + str(learnerId) + " Sublid " + str(subLid)
				minsub = sub
				minSubTime = subTime
				minLearnerId = subLid
		
		print "Debug 6 getSubmissionToReviewAndAddReviewer " + str(learnerId) 
		if minsub == None:
			return None

		print "Debug 7 getSubmissionToReviewAndAddReviewer " + str(learnerId) + "subLid " + str(minsub.getLearnerId())
		minsub.addReviewer(learnerId)

		return minsub



class LearnerState:
	WaitingBeforeFirstSubmission ,WorkingOnSubmission ,WaitingForSubmissionsToreview,Reviewing,Reviewed,WaitingForGrade,Finished = range(7)

class Learner:

	def __init__(self,learnerId,firstSubmissionStartTime,firstSubmissionTrueGrade,reviewBias,sim):
		self.lId = learnerId
		self.fSST = firstSubmissionStartTime
		self.fSTG = firstSubmissionTrueGrade
		self.rB = reviewBias
		self.state = LearnerState.WaitingBeforeFirstSubmission
		self.workToBeDone = 0
		self.workStart = 0
		self.workFinish = 0
		self.numSubmissions = 0
		self.numReviews = 0
		self.sim = sim
		self.LastSubmission = None
		self.submissionReviewing = None
		self.submissionsAlreadyReviewed = []

	def getTrueScoreForTheSubmission(self):

		return min(100,self.fSTG + 15*self.numSubmissions)

	def getGradeForTheSubmissionReviewing(self,trueScore):

		if self.rB < 0:
			return max(0,trueScore+self.rB)
		return min(100,trueScore+self.rB)

	def getState(self):
		return self.state

	def setWorkForSubmission(self,current_tick):
		self.workStart = current_tick
		self.workFinish = current_tick + 50

	def setWorkForReview(self,current_tick):
		self.workStart = current_tick
		self.workFinish = current_tick + 20



	def doTickWork(self,current_tick):

		print "Debug -1 In the beginning of tick " + str(self.lId) + " Current tick: " + str(current_tick)
		while 1:
			if current_tick < self.fSST:
				print "Debug 0 In the beginning of tick " + str(self.lId) + " Current tick: " + str(current_tick)
				break
			elif self.state == LearnerState.WaitingBeforeFirstSubmission:
				print "Debug 1 In the beginning of tick " + str(self.lId) + " Current tick: " + str(current_tick)
				self.state = LearnerState.WorkingOnSubmission
				self.setWorkForSubmission(current_tick)
				break
			elif self.state == LearnerState.WorkingOnSubmission:
				print "Debug 2  In the beginning of tick " + str(self.lId) + " Current tick: " + str(current_tick)
				#print "Debug Working on submission " + str(self.lId) + " work left " + str(self.workToBeDone)
				# self.workToBeDone = self.workToBeDone - 1

				# if self.workToBeDone >= 0:
				# 	break

				if current_tick < self.workFinish:
					break

				#TODO Done with work Submit it ?
				trueScore = self.getTrueScoreForTheSubmission()
				submission = Submission(current_tick,self.lId,trueScore)
				self.numSubmissions = self.numSubmissions + 1
				self.LastSubmission = submission
				self.sim.addSubmission(submission)
				self.state = LearnerState.WaitingForSubmissionsToreview
				continue
				print "Debug 2.5  In the beginning of tick " + str(self.lId) + " Current tick: " + str(current_tick)
				
			elif self.state == LearnerState.WaitingForSubmissionsToreview:

				print "Debug 3  In the beginning of tick " + str(self.lId) + " Current tick: " + str(current_tick)

				#Try to see if the last submission by me has been graded if failed work on it
				#self.state = LearnerState.WorkingOnSubmission
				#self.workToBeDone = 50
				#break
				if self.LastSubmission == None:
					break #error condition should not happen

				islastSubmissionGraded = self.LastSubmission.isPassingGrade() 
				if islastSubmissionGraded == 0:
					#Remove it from the list of submissions
					self.sim.removeFailedSubmission(self.lId)
					self.state = LearnerState.WorkingOnSubmission
					self.setWorkForSubmission(current_tick)
					break

				print "Debug 3.5  In the beginning of tick " + str(self.lId) + " Current tick: " + str(current_tick)

				#Try to see if something to review
				#self.state = LearnerState.Reviewing
				#self.workToBeDone = 20
				#break
				submissiontoReview = self.sim.getSubmissionToReviewAndAddReviewer(self.lId,self.submissionsAlreadyReviewed)
				if submissiontoReview == None:
					break
				
				print "Debug 3.75  In the beginning of tick " + str(self.lId) + " Current tick: " + str(current_tick)
				#self.sim.addReviewerForSubmission(submissiontoReview,self.lId)
				self.submissionReviewing = submissiontoReview
				self.submissionsAlreadyReviewed.append(submissiontoReview.getLearnerId())
				self.state = LearnerState.Reviewing
				self.setWorkForReview(current_tick)


				#If nothing keep waiting in this state

			elif self.state == LearnerState.Reviewing:

				print "Debug 4  In the beginning of tick " + str(self.lId) + " Current tick: " + str(current_tick)
				# self.workToBeDone = self.workToBeDone - 1
				# if self.workToBeDone >= 0:
				# 	break

				if current_tick < self.workFinish:
					break
				# 	self.state = LearnerState.Reviewed
				# 	break
				# elif self.state == LearnerState.Reviewed:

				print "Debug 4.25  In the beginning of tick " + str(self.lId) + " Current tick: " + str(current_tick)

				self.numReviews = self.numReviews + 1
				grade = self.getGradeForTheSubmissionReviewing(self.submissionReviewing.getTrueScore())
				self.submissionReviewing.addGrade(grade,current_tick)
				self.submissionReviewing = None


				#Try to see if the last submission by me has been graded if failed work on it
				#self.state = LearnerState.WorkingOnSubmission
				#self.workToBeDone = 50
				#break
				if self.LastSubmission == None:
					break #error condition should not happen

				print "Debug 4.5  In the beginning of tick " + str(self.lId) + " Current tick: " + str(current_tick)
				islastSubmissionGraded = self.LastSubmission.isPassingGrade() 
				if islastSubmissionGraded == 0:
					#Remove it from the list of submissions
					self.sim.removeFailedSubmission(self.lId)
					self.state = LearnerState.WorkingOnSubmission
					self.setWorkForSubmission(current_tick)
					break


				print "Debug 4.75  In the beginning of tick " + str(self.lId) + " Current tick: " + str(current_tick)
				if self.numReviews < 3*self.numSubmissions:
					self.state = LearnerState.WaitingForSubmissionsToreview
					print "Hello Debug"
					continue

				print "Debug 4.90  In the beginning of tick " + str(self.lId) + " Current tick: " + str(current_tick)
				#See if latest submission doesn't have a grade
				if islastSubmissionGraded == -1:
					self.state = LearnerState.WaitingForGrade
					continue

				print "Debug 4.95  In the beginning of tick " + str(self.lId) + " Current tick: " + str(current_tick)

				#If nothing it means got a passing grade 
				self.state = LearnerState.Finished
				break

			elif self.state == LearnerState.WaitingForGrade:

				print "Debug 5  In the beginning of tick " + str(self.lId) + " Current tick: " + str(current_tick)
				#Check how many reviews does latest submission has 
				#if less than 3 
				#break
				islastSubmissionGraded = self.LastSubmission.isPassingGrade()
				if islastSubmissionGraded == -1: #No grade for the latest submission
					break

				print "Debug 5.25  In the beginning of tick " + str(self.lId) + " Current tick: " + str(current_tick)
				#Try to see if the last submission by me has been graded if failed work on it
				#self.state = LearnerState.WorkingOnSubmission
				#self.workToBeDone = 50
				#break
				if islastSubmissionGraded == 0:
					self.sim.removeFailedSubmission(self.lId)
					self.state = LearnerState.WorkingOnSubmission
					#self.workToBeDone = 50
					self.setWorkForSubmission(current_tick)
					break

				print "Debug 5.50  In the beginning of tick " + str(self.lId) + " Current tick: " + str(current_tick)
				#If nothing it means got a passing grade 
				self.state = LearnerState.Finished
				break
			elif self.state == LearnerState.Finished:
				break





class Simulation:

	def __init__(self,duration):
		self.duration = duration
		self.ticks_elapsed = 0
		self.learners = []
		self.submissionPool = SubmissionPool()
		self.submissionsHistory = {}


	def addLearner(self,learner):
		self.learners.append(learner)

	def addSubmission(self,submission):

		print "Debug add submission"
		
		self.submissionPool.addSubmissionToPool(submission)

		#For pretty printing simulation state at the end
		submitterId = submission.getLearnerId()

		if submitterId not in self.submissionsHistory:
			self.submissionsHistory[submitterId] = []
		
		self.submissionsHistory[submitterId].append(submission)

	def removeFailedSubmission(self,submitterid):
		self.submissionPool.removeFailedSubmission(submitterid)

	def markReadyToReview(self):
		self.submissionPool.markSubmissionsReadyToReview()

	def getSubmissionToReviewAndAddReviewer(self,learnerId,submissionsAlreadyReviewed):

		return self.submissionPool.getSubmissionToReviewAndAddReviewer(learnerId,submissionsAlreadyReviewed)

	def markGradedSubmissions(self):
		self.submissionPool.markGradedSubmissions()

	def run(self):

		while self.duration > self.ticks_elapsed:


			#Mark all the submission in the last tick ready to be reviewed
			self.markReadyToReview()
			#self.markGradedSubmissions()

			learnerQueue = []
			for learner in self.learners:
				#first find learners which are in reviewing state or reviewed state and perform the tick for them
				learnerState = learner.getState() 
				if learnerState == LearnerState.Reviewing or learnerState == LearnerState.Reviewed:
					learnerQueue.insert(0,learner)
				else:
					learnerQueue.append(learner)


			for learner in learnerQueue:
				learner.doTickWork(self.ticks_elapsed)


			self.ticks_elapsed += 1

	def __repr__(self):

		retval = ''

		sorted_learner_ids = sorted(self.submissionsHistory.keys())

		
		print "Debug size of submissions done " + str(len(self.submissionsHistory.keys()))

		for lID in sorted_learner_ids:
			for idx in range(len(self.submissionsHistory[lID])):
				sub = self.submissionsHistory[lID][idx]
				if retval != '':
					retval = retval + '\n'

				retval = retval + str(lID) + ' ' + str(idx) + ' ' + str(sub.getSubmissionTime())\
					+ ' ' + str(sub.getGrade()) + ' ' + str(sub.getGradeTick())

		return retval

	__str__ = __repr__








if __name__ == '__main__':

	f = open('test_cases_80bf9f7km99/input009.txt','r')

	#duration = int(raw_input())
	#num_learners = int(raw_input())

	duration = int(f.readline())
	num_learners = int(f.readline())
	sim = Simulation(duration)

	for i in xrange(num_learners):
		learner_params = f.readline().split()

		lId = int(learner_params[0])
		fSST = int(learner_params[1])
		fSTG = int(learner_params[2])
		rB = int(learner_params[3])

		learner = Learner(lId,fSST,fSTG,rB,sim)

		sim.addLearner(learner)

	f.close()

	sim.run()

	print sim



