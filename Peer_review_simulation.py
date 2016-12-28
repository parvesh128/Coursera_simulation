

"""Peer review Simulation

   Classes used:-
   SubmissionState - Different States for a Submission.
   Submission - Represent attributes and functionalities for a submission.
   SubmissionNode - Double linked list(DLL) representation to store submission.
   SubmissionDLLAndMap - Encapsulates Double linked list of submissions and also a dict which maps
	learnerIDs to the submission nodes in DLL.
   SubmissionPool - Pool to store submitted/reviewed/graded submissions.
   LearnerState - Represent different states of a learner.
   Learner - Represent attributes and functionalities of a Learner.
   Simulation - Represent attributes and functionalities of the simulation.
"""
import sys



class SubmissionState:
	"""Represent different states for a Submission
	"""
	Submitted, ReadyToReview, BeingReviewedReviewersNeeded,\
		BeingReviewedNoMoreReviwersNeeded, GradeReady = range(5)


class Submission:
	
	def __init__(self, submissionTime, learnerId, trueScore):
		"""Constructor for a Submission  
		
		Args:
		    submissionTime (Integer): Time at which the submission was made.
		    learnerId (TYPE): ID for the student made the submission.
		    trueScore (TYPE): True score of the submission
		"""
		self.state = SubmissionState.Submitted
		self.submissionTime = submissionTime
		self.learnerId = learnerId
		self.grade = 0
		self.numReviewers = 0
		self.reviewsCompleted = 0
		self.trueScore = trueScore
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

	def addGrade(self, grade, current_tick):
		"""Add a Grade to the submission. Also if this is the third grade for 
		   submission, mark overall grade for the submission to be ready.
		
		Args:
		    grade (Integer): Value of the grade to be the added.
		    current_tick (TYPE): Current tick of the simulation.
		
		Returns:
		    None
		"""
		if self.state != SubmissionState.BeingReviewedReviewersNeeded and\
			self.state != SubmissionState.BeingReviewedNoMoreReviwersNeeded:
			# This means a learner is trying to add a grade for a submission
			# which is not ready for review, thus throwing an unhandled exception.
			raise Exception('Invalid state for submission in addGrade')

		self.reviewsCompleted += 1
		self.numReviewers -= 1

		if self.grade == -1:
			self.grade = grade
		else:
			self.grade += grade

		if self.reviewsCompleted == 3:
			self.state = SubmissionState.GradeReady
			self.gradeTick = current_tick

	def isPassingGrade(self):
		"""Check if the submission has passing grade
		
		Returns:
		    Integer: -1 if Grade not ready, 1 if yes, 0 if failing grade
		"""
		if self.state != SubmissionState.GradeReady:
			return -1

		if self.grade >= 240:
			return 1

		return 0

	def addReviewer(self, reviewerId):
		"""Add a reviewer for the submission. Also transition state for
		   submission when required number of reviewers are added.
		
		Args:
		    reviewerId (Integer): Learner ID for the reviewer
		
		"""
		if self.state != SubmissionState.ReadyToReview and self.state != SubmissionState.BeingReviewedReviewersNeeded:
			# This means a learner is trying to add reviewer for a submission
			# which is not ready for review, thus throwing an unhandled exception.
			raise Exception('Invalid state for submission in addReviewer')

		if self.state == SubmissionState.ReadyToReview:
			self.numReviewers = 1
			self.state = SubmissionState.BeingReviewedReviewersNeeded
		elif self.state == SubmissionState.BeingReviewedReviewersNeeded:
			self.numReviewers += 1
			if self.reviewsCompleted + self.numReviewers >= 3:
				self.state = SubmissionState.BeingReviewedNoMoreReviwersNeeded


class SubmissionNode:
	"""Double linked list(DLL) representation to store submission
	"""
	def __init__(self, submission):
		"""Constructor for DLL node.
		
		Args:
		    submission (Submision): Instance of Submission class
		"""
		self.sub = submission
		self.p = None
		self.n = None

	def getSubmission(self):
		return self.sub


class SubmissionDLLAndMap:
	def __init__(self):
		self.head = None
		self.tail = None
		self.map = {}
		self.size = 0
		self.current = -1

	def getSize(self):
		return self.size

	def __iter__(self):
		"""Return iterator to help iterate through DLL. 
		"""
		self.current = -1
		return self
	
	def next(self):
		"""Returns the next submission in DLL. This will be called when looping
		   through iterator returned by __iter__.
		"""
		retval = None 
		if self.current == -1:
			if self.head == None:
				raise StopIteration
			self.current = self.head.n
			retval = self.head.getSubmission()
		elif self.current is None:
			raise StopIteration
		else:
			retval = self.current.getSubmission()
			self.current = self.current.n
		return retval

	def insertNode(self, subNode):

		if subNode is None:
			# Invalid use case for this function - Trying to insert None thus
			# throwing an unhandled exception.
			raise Exception('Invalid submission node param in insertNode')

		self.map[subNode.getSubmission().getLearnerId()] = subNode

		if self.head is None and self.tail is None:
			self.head = subNode
			self.tail = subNode
		else:
			self.tail.n = subNode
			subNode.p = self.tail
			self.tail = subNode

		self.size += 1

	def insert(self, submission):

		if submission is None:
			# Invalid use case for this function - Trying to insert None thus
			# throwing an unhandled exception.
			raise Exception('Invalid submission param in insert')

		new_node = SubmissionNode(submission)

		self.insertNode(new_node)

	def remove(self, learnerId):

		if learnerId is None:
			# Invalid use case for this function - Trying to remove submission
			# of empty learner ID 
			raise Exception('Invalid submission param in insert')

		if learnerId not in self.map:
			raise Exception('Submission from learner with ID=%d not present in submission Pool' %(learnerId))

		submisisonNode = self.map[learnerId]

		if submisisonNode is None:
			# Invalid use case for this function - Trying to remove None thus
			# throwing an unhandled exception.
			raise Exception('Invalid submission node in removeNode')

		if self.size == 1:
			self.head = None
			self.tail = None
		else:
			prevNode = submisisonNode.p
			nextNode = submisisonNode.n

			if prevNode is not None:
				prevNode.n = nextNode
			if nextNode is not None:
				nextNode.p = prevNode

			if self.head == submisisonNode and prevNode is not None:
				self.head = prevNode
			elif self.head == submisisonNode:
				self.head = nextNode

			if self.tail == submisisonNode and nextNode is not None:
				self.tail = nextNode
			elif self.tail == submisisonNode:
				self.tail = prevNode

		self.size -= 1

		del self.map[learnerId]

	def appendOtherListandMap(self, other):
		"""Append one SubmissionDLLAndMap to other
		
		Args:
		    other (SubmissionDLLAndMap): List to be appended
		
		"""
		if other.size == 0:
			return

		temp = other.head

		while temp is not None:

			temp.sub.setState(SubmissionState.ReadyToReview)
			self.insertNode(temp)
			temp = temp.n


class SubmissionPool:
	"""Pool to store submitted/reviewed/graded submissions 
	"""
	def __init__(self):
		"""Initializing pool for submissions in different states
		"""
		self.subLM = SubmissionDLLAndMap()  #Submitted
		self.revLM = SubmissionDLLAndMap()  #Ready to review/Being reviewed/Graded 

	def addSubmissionToPool(self, submission):
		self.subLM.insert(submission)

	def removeFailedSubmission(self, submitterid):
		"""Removes failed submission.
		
		Args:
		    submitterid (Integer): LearnerID of the submitter
		
		"""
		self.revLM.remove(submitterid)

	def markSubmissionsReadyToReview(self):
		"""Move all submissions in submitted pool to the review pool
		
		"""
		if self.subLM.getSize() > 0:

			self.revLM.appendOtherListandMap(self.subLM)

			self.subLM = SubmissionDLLAndMap()

	def getSubmissionToReviewAndAddReviewer(self, learnerId, submissionsAlreadyReviewed):
		"""Get submission to review for the learner. If yes then add reviewer
		   for the submission as well.
		
		Args:
		    learnerId (Integer): ID for the learner who wants to review
		    submissionsAlreadyReviewed (List[learnerID]): List of learnerID of 
		    the submissions already reviewed by the learner.
		
		Returns:
		    Submission: instance of Submission class which learner will review.
		"""
		minsub = None
		minSubTime = sys.maxint
		minLearnerId = sys.maxint

		for sub in self.revLM:
			subLid = sub.getLearnerId()

			if subLid == learnerId:
				continue

			if subLid in submissionsAlreadyReviewed:
				continue

			subState = sub.getState()

			if subState != SubmissionState.ReadyToReview and subState != SubmissionState.BeingReviewedReviewersNeeded:
				continue

			subTime = sub.getSubmissionTime()
			if (subTime < minSubTime) or ((subTime == minSubTime) and (subLid < minLearnerId)):
				minsub = sub
				minSubTime = subTime
				minLearnerId = subLid
		
		if minsub is not None:
			minsub.addReviewer(learnerId)
		return minsub


class LearnerState:
	WaitingBeforeFirstSubmission, WorkingOnSubmission,\
		WaitingForSubmissionsToreview, Reviewing, DoneReviewing,\
		WaitingForGrade, Finished = range(7)


class Learner:
	
	def __init__(
		self, learnerId, firstSubmissionStartTime, firstSubmissionTrueGrade,
		reviewBias, sim):
		"""Initialize Learner Attributes
		
		Args:
		    learnerId (Integer): ID for the learner
		    firstSubmissionStartTime (Integer): First submission Start Time
		    firstSubmissionTrueGrade (Integer): True Grade for first submission
		    reviewBias (Integer): Review Bias in the range [-20,20]
		    sim (Simulation): Instance of the simulation for Callback
		"""
		self.lId = learnerId
		self.fSST = firstSubmissionStartTime
		self.fSTG = firstSubmissionTrueGrade
		self.rB = reviewBias
		self.state = LearnerState.WaitingBeforeFirstSubmission
		self.workStart = 0
		self.workFinish = 0
		self.numSubmissions = 0
		self.numReviews = 0
		self.sim = sim
		self.LastSubmission = None
		self.submissionReviewing = None
		self.submissionsAlreadyReviewed = []

	def getTrueScoreForTheSubmission(self):

		return min(100, self.fSTG + 15 * self.numSubmissions)

	def getGradeForTheSubmissionReviewing(self, trueScore):

		if self.rB < 0:
			return max(0, trueScore + self.rB)
		return min(100, trueScore + self.rB)

	def getState(self):
		return self.state

	def setWorkForSubmission(self, current_tick):
		"""Set up start and finish timestamp required for working on Submission.
		
		Args:
		    current_tick (Integer): current tick for the simulator
		
		"""
		self.workStart = current_tick
		self.workFinish = current_tick + 50

	def setWorkForReview(self, current_tick):
		"""Set up start and finish timestamp required for working on Review.
		
		Args:
		    current_tick (Integer): current tick for the simulator
		
		"""
		self.workStart = current_tick
		self.workFinish = current_tick + 20

	def checkLastSubmission(self):
		"""Check the status for last submission made by learner. 
		
		Returns:
		    Integer: -1 if no grade for last submission, 1 if passing grade,
		    0 if failing grade
		"""
		if self.LastSubmission is None:
			# This should not be called if no valid last submission, thus
			# raising an unhandled exception
			raise Exception('No Last submission to check state for')
		
		hasPassingGrade = self.LastSubmission.isPassingGrade() 
		
		return hasPassingGrade

	def removeLastSubmissionAndStartWorking(self, current_tick):
		"""Remove the last submission from the
		   submission pool and start working on the same.
		
		Args:
		    current_tick (Integer): current tick for the simulator
		
		"""
		self.sim.removeFailedSubmission(self.LastSubmission.getLearnerId())
		self.state = LearnerState.WorkingOnSubmission
		self.setWorkForSubmission(current_tick)

	def doReviewWork(self, current_tick):
		"""Work done by learner when in reviewing state. If learner is done, 
		   add the grade for the submission and then move it to Done reviewing
		   state.
		
		Args:
		    current_tick (Integer): current tick for the simulator
		
		"""
		if self.state != LearnerState.Reviewing:
			#This should not be called in learner not in reviewing state, thus
			#raising an unhandled exception.
			raise Exception('Invalid state for reviewer in doReviewWork')
		
		if current_tick < self.workFinish:
			return

		self.numReviews += 1
		grade = self.getGradeForTheSubmissionReviewing(
			self.submissionReviewing.getTrueScore())
		self.submissionReviewing.addGrade(grade, current_tick)
		self.submissionReviewing = None

		self.state = LearnerState.DoneReviewing

	def doTickWork(self, current_tick):
		"""Implementation of the state machine for Learner. This is called for
		   each learner every tick. 
		
		Args:
		    current_tick (Integer): current tick for the simulator
		
		"""
		while True:
			if current_tick < self.fSST and\
				self.state == LearnerState.WaitingBeforeFirstSubmission:
				#Keep waiting in the Initial state
				
				break
			elif self.state == LearnerState.WaitingBeforeFirstSubmission:
				#Learner can now start working on submission
				self.state = LearnerState.WorkingOnSubmission
				self.setWorkForSubmission(current_tick)
				
				break
			elif self.state == LearnerState.WorkingOnSubmission:
				# If not done with submission, stay in the same state.
				if current_tick < self.workFinish:
					break

				# Done with submission,let's submit it and start waiting for
				# submissions to review.
				trueScore = self.getTrueScoreForTheSubmission()
				submission = Submission(current_tick, self.lId, trueScore)
				self.numSubmissions = self.numSubmissions + 1
				self.LastSubmission = submission
				self.sim.addSubmission(submission)
				self.state = LearnerState.WaitingForSubmissionsToreview
				# Learner after submitting immediately starts waiting for
				# submissions to review, thus a continue here instead of break.
				# This way in the same tick itself, learner can perform actions
				# required in the WaitingForSubmissionsToreview state.
				continue
			elif self.state == LearnerState.WaitingForSubmissionsToreview:
				#Try to see if the last submission by me has been graded. 
				#If failing grade start work on it
				if self.checkLastSubmission() == 0:
					self.removeLastSubmissionAndStartWorking(current_tick)
					break

				# If passing grade or no grade for last submission, then try to
				# see if something to review
				submissiontoReview = \
					self.sim.getSubmissionToReviewAndAddReviewer(
						self.lId, self.submissionsAlreadyReviewed)
				
				if submissiontoReview is not None:
					self.submissionReviewing = submissiontoReview
					self.submissionsAlreadyReviewed.append(
						submissiontoReview.getLearnerId())
					self.state = LearnerState.Reviewing
					self.setWorkForReview(current_tick)
				
				break
			elif self.state == LearnerState.Reviewing:
				# No work needs to be done here for Reviewing state, actual work
				# for this state is done in doReviewWork.
				break
			elif self.state == LearnerState.DoneReviewing:
				#Try to see if the last submission by me has been graded. 
				#If failing grade start work on it
				hasPassingGrade = self.checkLastSubmission()
				if hasPassingGrade == 0:
					self.removeLastSubmissionAndStartWorking(current_tick)
					break
				
				# If passing grade for the last submission, then see if learner
				# needs to review more. If yes continue from here, since learner
				# needs to immediately start waiting for submissions to review.
				if self.numReviews < 3 * self.numSubmissions:
					self.state = LearnerState.WaitingForSubmissionsToreview
					continue
				
				# If no grade for the last submission and  no more review needs
				# to be done then immediately(thus continue) start waiting for
				# grade. 
				if hasPassingGrade == -1:
					self.state = LearnerState.WaitingForGrade
					continue

				# If no pending actions then learner is finished 
				self.state = LearnerState.Finished
				
				break
			elif self.state == LearnerState.WaitingForGrade:
				# Keep waiting in the same state if last submission doesn't have
				# grade. 
				hasPassingGrade = self.checkLastSubmission()
				if hasPassingGrade == -1:
					break
				
				# If failing grade for the last submission, then start working
				# on it.
				if hasPassingGrade == 0:
					self.removeLastSubmissionAndStartWorking(current_tick)
					break
				
				#If no pending actions learner is finished
				self.state = LearnerState.Finished

				break
			elif self.state == LearnerState.Finished:
				# Do nothing in Finished state
				break


class Simulation:

	def __init__(self, duration):
		"""Initialize Simulation state
		
		Args:
		    duration (Integer): Number of ticks for which simulator needs to run
		"""
		self.duration = duration
		self.ticks_elapsed = 0
		self.learners = []
		self.submissionPool = SubmissionPool()
		self.submissionsHistory = {}  #Map to store history of submissions.

	def addLearner(self, learner):
		self.learners.append(learner)

	def addSubmission(self, submission):
		"""Add Submission to the submission pool as well as to the Submission
		   history
		
		Args:
		    submission (Submission): Submission to be added

		"""		
		self.submissionPool.addSubmissionToPool(submission)

		submitterId = submission.getLearnerId()
		if submitterId not in self.submissionsHistory:
			self.submissionsHistory[submitterId] = []
		self.submissionsHistory[submitterId].append(submission)

	def removeFailedSubmission(self, submitterid):
		"""Remove submission from the submission pool
		
		Args:
		    submitterid (Integer): Learner ID for the submission
		
		"""
		self.submissionPool.removeFailedSubmission(submitterid)

	def markReadyToReview(self):
		"""Mark submitted submissions in the submissions Pool to ready to review
		"""
		self.submissionPool.markSubmissionsReadyToReview()

	def getSubmissionToReviewAndAddReviewer(
		self, learnerId, submissionsAlreadyReviewed):
		""" Get submission to reivew for a learner and also mark the reviewer.
		
		Args:
		    learnerId (Integer): ID of the learner
		    submissionsAlreadyReviewed (List[ID]): List of IDs of the
		    submissions already reviewed by the learner
		
		Returns:
		    Submission: Submission which learner will review
		"""
		return self.submissionPool.getSubmissionToReviewAndAddReviewer(
			learnerId, submissionsAlreadyReviewed)

	def run(self):
		"""Main driver function for the Simulation.
		   This would run for duration specified in the input
		
		"""
		while self.duration > self.ticks_elapsed:


			# Mark all the submissions in the last tick ready to be reviewed
			self.markReadyToReview()

			ReviewingLearners = []
			for learner in self.learners:
				# Find learners which are in reviewing state 
				learnerState = learner.getState() 
				if learnerState == LearnerState.Reviewing:
					ReviewingLearners.append(learner)
				

			# In each tick, first let all the reviewers perform their tasks for
			# the tick. This is needed because learners who need to check if
			# their latest submission grade needs to take into account
			# actions of all other learners.
			for learner in ReviewingLearners:
				learner.doReviewWork(self.ticks_elapsed)

			# Then let all the learners perform their actions for the tick
			for learner in self.learners:
				learner.doTickWork(self.ticks_elapsed)

			self.ticks_elapsed += 1

	def __repr__(self):
		"""Pretty printing simulation state at the end.
		
		Returns:
		    str: String representation of the simulation ran.
		"""
		retval = ''

		sorted_learner_ids = sorted(self.submissionsHistory.keys())

		for lID in sorted_learner_ids:
			for idx in range(len(self.submissionsHistory[lID])):
				sub = self.submissionsHistory[lID][idx]

				retval += str(lID) + ' ' + str(idx) + ' ' + str(sub.getSubmissionTime())\
					+ ' ' + str(sub.getGrade()) + ' ' + str(sub.getGradeTick()) + '\n'

		return retval

	__str__ = __repr__

if __name__ == '__main__':
	"""Main function to read input and start simulation
	"""
	
	duration = int(raw_input())
	num_learners = int(raw_input())

	sim = Simulation(duration)

	for i in xrange(num_learners):
		learner_params = raw_input().split()

		lId = int(learner_params[0])
		fSST = int(learner_params[1])
		fSTG = int(learner_params[2])
		rB = int(learner_params[3])

		learner = Learner(lId,fSST,fSTG,rB,sim)

		sim.addLearner(learner)


	sim.run()
	sys.stdout.write(str(sim))
	sys.stdout.flush()



