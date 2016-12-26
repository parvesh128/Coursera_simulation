import sys


class SubmissionState:
	Start,WorkedOn,Submitted ,ReadyToReview ,BeingReviewedReviewersNeeded,BeingReviewedNoMoreReviwersNeeded,GradeReady = range(8)


class Submission:

	def __init__(self,submissionTime,learnerId, trueScore):

		self.state = SubmissionState.Start
		self.submissionTime = 0
		self.learnerId = learnerId
		self.grade = 0
		self.numReviewers = 0
		self.reviewsCompleted = 0
		self.trueScore = trueScore
		self.reviewers = []
		self.gradeTick =

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

	def getSubmissionTime(self):
		return self.submissionTime


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

		if self.state == Submission.GradeReady:
			return self.grade

		return -1

	def isPassingGrade(self):

		if self.state != Submission.GradeReady:
			return -1

		if self.grade >= 240:
			return 1

		return 0

	def getReviewers(self):
		return self.reviewers

	def addReviewer(self,reviewerId):

		if self.state != ReadyToReview and self.state != BeingReviewedReviewersNeeded:
			return -1  #Should not happen

		if self.state == SubmissionState.ReadyToReview:
			self.reviewers.append[reviewerId]
			self.numReviewers = 1
			self.state = SubmissionState.BeingReviewedReviewersNeeded
		elif self.state == SubmissionState.BeingReviewedReviewersNeeded:
			self.reviewers.append[reviewerId]
			self.numReviewers = self.numReviewers + 1
			if self.reviewsCompleted + self.numReviewers == 3:
				self.state = SubmissionState.BeingReviewedNoMoreReviwersNeeded







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


	def addSubmissionToPool(self,submission):
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



	def getSubmissionToReviewAndAddReviewer(self,learnerId,submissionsAlreadyReviewed):

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



class LearnerState:
	WaitingBeforeFirstSubmission ,WorkingOnSubmission ,WaitingForSubmissionsToreview,Reviewing,WaitingForGrade,Finished = range(6)

class Learner:

	def __init__(self,learnerId,firstSubmissionStartTime,firstSubmissionTrueGrade,reviewBias,sim):
		self.lId = learnerId
		self.fSST = firstSubmissionStartTime
		self.fSTG = firstSubmissionTrueGrade
		self.rB = reviewBias
		self.state = LearnerState.WaitingBeforeFirstSubmission
		self.workToBeDone = 0
		self.numSubmissions = 0
		self.numReviews = 0
		self.sim = sim
		self.LastSubmission = None
		self.submissionReviewing = None
		self.submissionsAlreadyReviewed = []

	def getTrueScoreForTheSubmission(self):

		return min(100,self.fSTG + 15*self.numSubmissions)

	def getGradeForTheSubmissionReviewing(trueScore):

		if self.reviewBias > 0:

			return max(0,trueScore+reviewBias)

		return min(100,trueScore+reviewBias)

	def doTickWork(self,current_tick):

		while 1:
			if current_tick < self.fSTG:
				break
			elif self.state == LearnerState.WaitingBeforeFirstSubmission:
				self.state = LearnerState.WorkingOnSubmission
				self.workToBeDone = 50 #Start working on submisison
			elif self.state == LearnerState.WorkingOnSubmission:
				self.workToBeDone = self.workToBeDone - 1

				if self.workToBeDone > 0:
					break

				#TODO Done with work Submit it ?
				trueScore = self.getTrueScoreForTheSubmission()
				submission = Submission(current_tick,self.learnerId,trueScore)
				self.numSubmissions = self.numSubmissions + 1
				self.LastSubmission = submission
				self.sim.addSubmission(submission)
				self.state = LearnerState.WaitingForSubmissionsToreview
			
			elif self.state == LearnerState.WaitingForSubmissionsToreview:

				#Try to see if the last submission by me has been graded if failed work on it
				#self.state = LearnerState.WorkingOnSubmission
				#self.workToBeDone = 50
				#break
				if self.LastSubmission == None:
					break #error condition should not happen

				lastSubmissionGraded = self.LastSubmission.isPassingGrade() 
				if lastSubmissionGraded == 0:
					#Remove it from the list of submissions
					self.sim.removeFailedSubmission(self.lId)
					self.state = LearnerState.WorkingOnSubmission
					self.workToBeDone = 50
					break


				#Try to see if something to review
				#self.state = LearnerState.Reviewing
				#self.workToBeDone = 20
				#break
				submissiontoReview = self.sim.getSubmissionToReviewAndAddReviewer(self.lId,self.submissionsAlreadyReviewed)
				if submissiontoReview == None:
					break
				
				#self.sim.addReviewerForSubmission(submissiontoReview,self.lId)
				self.submissionReviewing = submissiontoReview
				self.submissionsAlreadyReviewed.append(submission.learnerId)
				self.state = LearnerState.Reviewing
				self.workToBeDone = 20


				#If nothing keep waiting in this state

			elif self.state == LearnerState.Reviewing:

				self.workToBeDone = self.workToBeDone - 1
				if self.workToBeDone > 0:
					break


				self.numReviews = self.numReviews + 1
				grade = getGradeForTheSubmissionReviewing(self.submissionReviewing.getTrueScore())
				self.submissionReviewing.addGrade(grade,current_tick)
				self.submissionReviewing = None


				#Try to see if the last submission by me has been graded if failed work on it
				#self.state = LearnerState.WorkingOnSubmission
				#self.workToBeDone = 50
				#break
				if self.LastSubmission == None:
					break #error condition should not happen

				lastSubmissionGraded = self.LastSubmission.isPassingGrade() 
				if lastSubmissionGraded == 0:
					#Remove it from the list of submissions
					self.sim.removeFailedSubmission(self.lId)
					self.state = LearnerState.WorkingOnSubmission
					self.workToBeDone = 50
					break


				if self.numReviews < 3*numSubmissions:
					self.state = LearnerState.WaitingForSubmissionsToreview
					break

				#See if latest submission doesn't have a grade
				if lastSubmissionGraded == -1:
					self.state = LearnerState.WaitingForGrade
					break


				#If nothing it means got a passing grade 
				self.state = Finished

			elif self.state == LearnerState.WaitingForGrade:


				#Check how many reviews does latest submission has 
				#if less than 3 
				#break
				lastSubmissionGraded = self.LastSubmission.isPassingGrade()
				if lastSubmissionGraded == -1:
					break


				#Try to see if the last submission by me has been graded if failed work on it
				#self.state = LearnerState.WorkingOnSubmission
				#self.workToBeDone = 50
				#break
				if lastSubmissionGraded == 0:
					self.sim.removeFailedSubmission(self.lId)
					self.state = LearnerState.WorkingOnSubmission
					self.workToBeDone = 50
					break


				#If nothing it means got a passing grade 
				self.state = Finished





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
		self.submissionPool.addSubmissionToPool(submission)

		#For pretty printing simulation state at the end
		submitterId = submission.getLearnerId()

		if submitterid not in self.submissionsHistory:
			self.submissionsHistory[submitterid] = []
		
		self.submissionsHistory[submitterid].append(submission)

	def removeFailedSubmission(self,submitterid):
		self.submissionPool.removeFailedSubmission(submitterid)

	def markReadyToReview(self):
		self.submissionPool.markSubmissionsReadyToReview()

	def getSubmissionToReviewAndAddReviewer(self,learnerId,submissionsAlreadyReviewed):

		self.submissionPool.getSubmissionToReviewAndAddReviewer(learnerId,submissionsAlreadyReviewed)

	def markGradedSubmissions(self):
		self.submissionPool.markGradedSubmissions()

	def run(self):

		while self.duration >= self.ticks_elapsed:


			#Mark all the submission in the last tick ready to be reviewed
			self.markReadyToReview()
			self.markGradedSubmissions()

			for learner in self.learners:
				learner.doTickWork(self.ticks_elapsed)

			self.ticks_elapsed += 1

	def __repr__(self):

		retval = ''

		sorted_learner_ids = sorted(self.submissionsHistory.keys())

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

	duration = int(raw_input())
	num_learners = int(raw_input())

	sim = Simulation(duration)

	for i in xrange(num_learners):
		learner_params = raw_input().split()

		lId = int(learner_params[0])
		fSST = int(learner_params[1])
		fSTG = int(learner_params[2])
		rB = int(learner_params[3])

		learner = Learner(lId,fSST,fSTG,rB)

		sim.addLearner(learner)

	sim.run()



