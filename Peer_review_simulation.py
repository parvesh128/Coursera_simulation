import sys
from enum import Enum


class LearnerState(Enum):
	WaitingBeforeFirstSubmission = 1
	WorkingOnSubmission = 2
	WaitingForSubmissionsToreview = 3
	Reviewing = 4
	WaitingForGrade = 5
	Finished = 6

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

	def getTrueScoreForTheSubmission(self):

		return min(100,self.fSTG + 15*self.numSubmissions)

	def getGradeForTheSubmission(trueScore):

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
				submisison = Submission(current_tick,self.learnerId,trueScore)
				self.numSubmissions = self.numSubmissions + 1
				self.LastSubmission = submisison
				self.sim.addsubmission(submisison)

				self.state = LearnerState.WaitingForSubmissionsToreview
			elif self.state == LearnerState.WaitingForSubmissionsToreview:

				#Try to see if the last submission by me has been graded if failed work on it
				#self.state = LearnerState.WorkingOnSubmission
				#self.workToBeDone = 50
				#break
				if self.LastSubmission == None:
					break #error condition should not happen
				if self.LastSubmission.isPassingGrade() == 0:
					#Remove it from the list of submissions
					self.sim.removeSubmission(self.LastSubmission)
					self.state = LearnerState.WorkingOnSubmission
					self.workToBeDone = 50
					break


				#Try to see if something to review
				#self.state = LearnerState.Reviewing
				#self.workToBeDone = 20
				#break
				submissiontoReview = self.sim.getSubmissionToReview()
				if submissiontoReview == None:
					break
				
				self.sim.addReviewerForSubmission(submissiontoReview,self.lId)
				self.submissionReviewing = submissiontoReview
				self.state = LearnerState.Reviewing
				self.workToBeDone = 20


				#If nothing keep waiting in this state

			elif self.state == LearnerState.Reviewing:

				self.workToBeDone = self.workToBeDone - 1
				if self.workToBeDone > 0:
					break


				self.numReviews = self.numReviews + 1
				grade = getGradeForTheSubmission(self.submissionReviewing.getTrueScore())
				self.submissionReviewing.addGrade(grade)
				self.submissionReviewing = None


				#Try to see if the last submission by me has been graded if failed work on it
				#self.state = LearnerState.WorkingOnSubmission
				#self.workToBeDone = 50
				#break

				if self.numReviews < 3*numSubmissions:
					self.state = LearnerState.WaitingForSubmissionsToreview

				#See if latest submission doesn't have a grade
				self.state = LearnerState.WaitingForGrade


				#If nothing it means got a passing grade 
				self.state = Finished

			elif self.state == LearnerState.WaitingForGrade:


				#Check how many reviews does latest submission has 
				#if less than 3 
				#break

				#Try to see if the last submission by me has been graded if failed work on it
				#self.state = LearnerState.WorkingOnSubmission
				#self.workToBeDone = 50
				#break

				#If nothing it means got a passing grade 
				self.state = Finished









class SubmissionState(Enum):
	Start = 1
	WorkedOn = 2
	Submitted = 3
	ReadyToReview = 5
	BeingReviewedReviewersNeeded = 6
	BeingReviewedNoMoreReviwersNeeded = 7
	GradeReady = 8




class Submission:

	def __init__(self,submissionTime,learnerId, trueScore):

		self.state = SubmissionState.Start
		self.submissionTime = 0
		self.learnerId = 
		self.grade = -1
		self.numReviewers = 0
		self.reviewsCompleted = 0
		self.trueScore = trueScore

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

	def addGrade(self,grade):

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


	def addReviewer(self):

		if self.state != ReadyToReview and self.state != BeingReviewedReviewersNeeded:
			return -1  #Should not happen

		if self.state == SubmissionState.ReadyToReview:
			self.numReviewers = 1
			self.state = SubmissionState.BeingReviewedReviewersNeeded
		elif self.state == SubmissionState.BeingReviewedReviewersNeeded:
			self.numReviewers = self.numReviewers + 1
			if self.reviewsCompleted + self.numReviewers == 3:
				self.state = SubmissionState.BeingReviewedNoMoreReviwersNeeded








class Simulation:

	def __init__(self,duration):
		self.duration = duration
		self.ticks_elapsed = 0
		self.learners = []
		self.submissions = []
		self.submissionsReadyToReview = []
		self.ReviewerSubmissionMap = {}
		self.submissionIndexMap = {}


	def addLearner(self,learner):
		self.learners.append(learner)

	# def addsubmission(self,submission):
	# 	self.submissions.append(submission)

	# 	submitterId = submisison.getLearnerId()

	# 	self.submissionIndexMap[submitterId] = len(self.submisisons) -1


	# def removeSubmission(self,submission):

	# 	submitterid = submission.getLearnerId()

	# 	index = self.submissionIndexMap[submitterId]

	# 	if index < 0:
	# 		return -1 #Error should not happen

	# 	self.submisisons.pop(index)

	# 	self.submissionIndexMap[submitterId] = -1




	# def markSubmissionsReadyToReview(self):

	# 	for sub in self.submissions:
	# 		if sub.getState() == SubmissionState.Submitted :
	# 			sub.setState(SubmissionState.ReadyToReview)

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




	def doTickWork(self):

		while self.duration >= self.ticks_elapsed:

			#Mark all the submission in the last tick ready to be reviewed




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



