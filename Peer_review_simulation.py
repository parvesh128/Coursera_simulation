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

				#TODO Done with work Submit it
				submisison = Submission(current_tick,self.learnerId)
				self.numSubmissions = self.numSubmissions + 1

				self.state = LearnerState.WaitingForSubmissionsToreview
			elif self.state == LearnerState.WaitingForSubmissionsToreview:

				#Try to see if the last submission by me has been graded if failed work on it
				#self.state = LearnerState.WorkingOnSubmission
				#self.workToBeDone = 50
				#break


				#Try to see if something to review
				#self.state = LearnerState.Reviewing
				#self.workToBeDone = 20
				#break

				#If nothing keep waiting in this state

			elif self.state == LearnerState.Reviewing:

				self.workToBeDone = self.workToBeDone - 1
				if self.workToBeDone > 0:
					break

				self.numReviews = self.numReviews + 1

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
	ReviewDone = 8




class Submission:

	def __init__(self,submissionTime,learnerId):

		self.state = SubmissionState.Start
		self.submissionTime = 0
		self.learnerId = 
		self.grade = -1
		self.numReviewers = 0



	def getLearnerId(self):
		return self.learnerId

	def getSubmissionTime(self):
		return self.submissionTime


	def getState(self):
		return self.state

	def setState(self,state):
		self.state = state




class Simulation:

	def __init__(self,duration):
		self.duration = duration
		self.ticks_elapsed = 0
		self.learners = []
		self.submissions = []
		self.submissionsReadyToReview = []

	def addLearner(self,learner):
		self.learners.append(learner)

	def addsubmission(self,submission):
		self.submissions.append(submission)

	def markSubmissionsReadyToReview(self):

		for sub in self.submissions:
			if sub.getState() == SubmissionState.Submitted :
				sub.setState(SubmissionState.ReadyToReview)

	def getSubmissionToReview(self,learnerId):

		subId = -1
		minSubTime = sys.maxint
		minLearnerId = sys.maxint

		for idx in xrange(len(self.submissions)):
			sub = self.submissions[idx]
			subLid = sub.getLearnerId()
			if subLid == learnerId :
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

		return self.submissions[subId]




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



