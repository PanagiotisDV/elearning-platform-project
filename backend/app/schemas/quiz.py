"""
SCHEMAS ΓΙΑ QUIZZES
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Any, Union
from datetime import datetime
from enum import Enum
import re  


class QuestionType(str, Enum):
    """Τύποι ερωτήσεων που υποστηρίζονται"""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_BLANK = "fill_blank"
    ESSAY = "essay"
    
    
    @classmethod
    def requires_options(cls, question_type: str) -> bool:
        """Επιστρέφει True αν ο τύπος ερώτησης απαιτεί επιλογές"""
        return question_type in [cls.MULTIPLE_CHOICE, cls.TRUE_FALSE]

# ========================================
# 2. QUESTION SCHEMAS
# ========================================
class QuestionCreate(BaseModel):
    """Δημιουργία ερώτησης"""
    model_config = ConfigDict(extra='forbid')      
    question_text: str = Field(
        ..., 
        min_length=3,  
        max_length=1000,  
        description="Το κείμενο της ερώτησης"
    )
    question_type: QuestionType = Field(
        default=QuestionType.MULTIPLE_CHOICE,
        description="Ο τύπος της ερώτησης"
    )
    options: Optional[List[str]] = Field(
        None,
        min_length=2,  
        max_length=10,  
        description="Επιλογές για πολλαπλή επιλογή"
    )
    correct_answer: str = Field(
        ..., 
        min_length=1,  
        max_length=500,  
        description="Η σωστή απάντηση"
    )
    points: int = Field(
        default=1, 
        ge=1, 
        le=100,  
        description="Πόντοι για την ερώτηση"
    )
    order: int = Field(
        default=0, 
        ge=0, 
        description="Σειρά εμφάνισης"
    )
   
    @field_validator('options')
    @classmethod
    def validate_options(cls, v: Optional[List[str]], info) -> Optional[List[str]]:
        """Επικύρωση των options βάσει του question_type"""
        question_type = info.data.get('question_type')
        
        if QuestionType.requires_options(question_type):
            if not v or len(v) < 2:
                raise ValueError(
                    f"Ο τύπος {question_type} απαιτεί τουλάχιστον 2 επιλογές"
                )
            
            cleaned_options = [opt.strip() for opt in v if opt.strip()]
            if len(cleaned_options) != len(set(cleaned_options)):
                raise ValueError("Οι επιλογές δεν μπορεί να έχουν διπλότυπες τιμές")
            
            correct_answer = info.data.get('correct_answer')
            if correct_answer and correct_answer not in cleaned_options:
                raise ValueError("Η σωστή απάντηση πρέπει να υπάρχει στις επιλογές")
            
            return cleaned_options
        
       
        if v is not None:
            raise ValueError(f"Ο τύπος {question_type} δεν επιτρέπει options")
        
        return v
    
    
    @field_validator('correct_answer')
    @classmethod
    def validate_correct_answer(cls, v: str, info) -> str:
        """Επικύρωση σωστής απάντησης βάσει τύπου"""
        question_type = info.data.get('question_type')
        
       
        if question_type == QuestionType.TRUE_FALSE:
            if v.lower() not in ['true', 'false']:
                raise ValueError("Για true/false, η απάντηση πρέπει να είναι 'True' ή 'False'")
            return v.capitalize()  
        
       
        if question_type == QuestionType.FILL_BLANK:
            v = v.strip()
            if not v:
                raise ValueError("Η σωστή απάντηση δεν μπορεί να είναι κενή")
        
        return v

class QuestionResponse(BaseModel):
    """Απάντηση για ερώτηση (χωρίς σωστή απάντηση - για μαθητές)"""
    model_config = ConfigDict(from_attributes=True)  
    id: int = Field(..., description="Μοναδικό ID ερώτησης")
    quiz_id: int = Field(..., description="ID του quiz που ανήκει")
    question_text: str = Field(..., description="Το κείμενο της ερώτησης")
    question_type: QuestionType = Field(..., description="Ο τύπος της ερώτησης")
    options: Optional[List[str]] = Field(None, description="Διαθέσιμες επιλογές")
    points: int = Field(..., description="Πόντοι της ερώτησης")
    order: int = Field(..., description="Σειρά εμφάνισης")
    
    
    @property
    def is_multiple_choice(self) -> bool:
        """Επιστρέφει True αν είναι ερώτηση πολλαπλής επιλογής"""
        return self.question_type == QuestionType.MULTIPLE_CHOICE

class QuestionWithAnswer(QuestionResponse):
    """Ερώτηση με σωστή απάντηση (για instructors)"""
    correct_answer: str = Field(
        ..., 
        description="Η σωστή απάντηση (ορατή μόνο σε instructors)"
    )
    
    @field_validator('correct_answer')
    @classmethod
    def validate_correct_answer_in_options(cls, v: str, info) -> str:
        """Ελέγχει ότι η σωστή απάντηση υπάρχει στις επιλογές για multiple_choice"""
        options = info.data.get('options')
        question_type = info.data.get('question_type')
        
        if question_type == QuestionType.MULTIPLE_CHOICE and options:
            if v not in options:
                raise ValueError("Η σωστή απάντηση πρέπει να υπάρχει στις επιλογές")
        
        return v

# ========================================
# 3. QUIZ SCHEMAS
# ========================================
class QuizCreate(BaseModel):
    """Δημιουργία quiz"""
    model_config = ConfigDict(extra='forbid')  
    
    title: str = Field(
        ..., 
        min_length=3,  
        max_length=200,
        description="Τίτλος του quiz"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,  
        description="Περιγραφή του quiz"
    )
    time_limit_minutes: int = Field(
        default=0, 
        ge=0, 
        le=300,  
        description="Χρονικό όριο σε λεπτά (0 = χωρίς όριο)"
    )
    passing_score: int = Field(
        default=70, 
        ge=0, 
        le=100,
        description="Ποσοστό επιτυχίας (0-100)"
    )
    max_attempts: int = Field(
        default=3, 
        ge=1, 
        le=10,  
        description="Μέγιστος αριθμός προσπαθειών"
    )
    is_published: bool = Field(
        default=False,
        description="Αν είναι δημοσιευμένο και ορατό σε μαθητές"
    )
    questions: List[QuestionCreate] = Field(
        default=[], 
        min_length=1,  
        max_length=100,  
        description="Οι ερωτήσεις του quiz"
    )
    
    
    @field_validator('questions')
    @classmethod
    def validate_total_points(cls, v: List[QuestionCreate]) -> List[QuestionCreate]:
        """Επικύρωση ότι οι συνολικοί πόντοι δεν ξεπερνούν ένα όριο"""
        if not v:
            raise ValueError("Το quiz πρέπει να έχει τουλάχιστον μία ερώτηση")
        
        total_points = sum(q.points for q in v)
        if total_points > 1000:  
            raise ValueError("Οι συνολικοί πόντοι του quiz δεν μπορούν να ξεπερνούν τους 1000")
        
        return v

class QuizUpdate(BaseModel):
    """Ενημέρωση quiz (όλα τα πεδία προαιρετικά)"""
    model_config = ConfigDict(extra='forbid')  
    
    title: Optional[str] = Field(
        None,
        min_length=3, 
        max_length=200,
        description="Νέος τίτλος"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Νέα περιγραφή"
    )
    time_limit_minutes: Optional[int] = Field(
        None,
        ge=0,
        le=300,
        description="Νέο χρονικό όριο"
    )
    passing_score: Optional[int] = Field(
        None,
        ge=0,
        le=100,
        description="Νέο ποσοστό επιτυχίας"
    )
    max_attempts: Optional[int] = Field(
        None,
        ge=1,
        le=10,
        description="Νέος μέγιστος αριθμός προσπαθειών"
    )
    is_published: Optional[bool] = Field(
        None,
        description="Αλλαγή κατάστασης δημοσίευσης"
    )
    
   
    @field_validator('title')
    @classmethod
    def validate_update_fields(cls, v, info) -> str:
        """Ελέγχει ότι υπάρχει τουλάχιστον ένα πεδίο προς ενημέρωση"""
        return v

class QuizResponse(BaseModel):
    """Απάντηση για quiz (για μαθητές)"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="Μοναδικό ID quiz")
    title: str = Field(..., description="Τίτλος quiz")
    description: Optional[str] = Field(None, description="Περιγραφή")
    lesson_id: int = Field(..., description="ID μαθήματος")
    time_limit_minutes: int = Field(..., description="Χρονικό όριο")
    passing_score: int = Field(..., description="Ποσοστό επιτυχίας")
    max_attempts: int = Field(..., description="Μέγιστες προσπάθειες")
    is_published: bool = Field(..., description="Κατάσταση δημοσίευσης")
    created_at: datetime = Field(..., description="Ημερομηνία δημιουργίας")
    updated_at: Optional[datetime] = Field(None, description="Ημερομηνία ενημέρωσης")
    questions: List[QuestionResponse] = Field(
        default=[], 
        description="Ερωτήσεις (χωρίς απαντήσεις)"
    )
    
   
    @property
    def total_points(self) -> int:
        """Συνολικοί πόντοι του quiz"""
        return sum(q.points for q in self.questions)
    
    @property
    def question_count(self) -> int:
        """Αριθμός ερωτήσεων"""
        return len(self.questions)
    
    @property
    def is_timed(self) -> bool:
        """Αν έχει χρονικό περιορισμό"""
        return self.time_limit_minutes > 0

class QuizDetailResponse(QuizResponse):
    """Πλήρες quiz με σωστές απαντήσεις (για instructors)"""
    model_config = ConfigDict(from_attributes=True)
    
    questions: List[QuestionWithAnswer] = Field(
        default=[], 
        description="Ερωτήσεις με σωστές απαντήσεις"
    )
    
    @property
    def question_types_summary(self) -> dict:
        """Σύνοψη τύπων ερωτήσεων"""
        summary = {}
        for q in self.questions:
            q_type = q.question_type.value
            summary[q_type] = summary.get(q_type, 0) + 1
        return summary

# ========================================
# 4. QUIZ ATTEMPT SCHEMAS
# ========================================
class QuizSubmit(BaseModel):
    """Υποβολή απαντήσεων"""
    model_config = ConfigDict(extra='forbid')  # ΠΡΟΣΘΗΚΗ
    
    answers: List[Any] = Field(
        ..., 
        min_length=1,  
        description="Οι απαντήσεις του χρήστη"
    )
    
    
    @field_validator('answers')
    @classmethod
    def validate_answers(cls, v: List[Any]) -> List[Any]:
        """Επικύρωση των απαντήσεων"""
        if not v:
            raise ValueError("Πρέπει να υποβληθεί τουλάχιστον μία απάντηση")
        
       
        cleaned_answers = []
        for answer in v:
            if isinstance(answer, str):
                cleaned = answer.strip()
                if cleaned:  # Μόνο μη-κενές απαντήσεις
                    cleaned_answers.append(cleaned)
            else:
                cleaned_answers.append(answer)
        
        return cleaned_answers

class QuizAttemptResponse(BaseModel):
    """Απάντηση για προσπάθεια"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="Μοναδικό ID προσπάθειας")
    user_id: int = Field(..., description="ID μαθητή")
    quiz_id: int = Field(..., description="ID quiz")
    score: int = Field(..., description="Πόντοι που πέτυχε")
    max_score: int = Field(..., description="Μέγιστοι πόντοι")
    percentage: int = Field(..., ge=0, le=100, description="Ποσοστό επιτυχίας")
    is_passed: bool = Field(..., description="Αν πέτυχε το quiz")
    answers: Optional[List[Any]] = Field(None, description="Οι απαντήσεις που έδωσε")
    started_at: datetime = Field(..., description="Ώρα έναρξης")
    completed_at: Optional[datetime] = Field(None, description="Ώρα ολοκλήρωσης")
    
    
    @property
    def time_spent_seconds(self) -> Optional[int]:
        """Δευτερόλεπτα που αφιέρωσε στην προσπάθεια"""
        if self.completed_at and self.started_at:
            return int((self.completed_at - self.started_at).total_seconds())
        return None
    
    @property
    def is_completed(self) -> bool:
        """Αν η προσπάθεια έχει ολοκληρωθεί"""
        return self.completed_at is not None
    
    @property
    def status(self) -> str:
        """Κατάσταση προσπάθειας"""
        if not self.is_completed:
            return "in_progress"
        return "passed" if self.is_passed else "failed"

# ========================================
# 5. ΠΡΟΣΘΗΚΗ: ΣΧΗΜΑΤΑ ΓΙΑ ΣΤΑΤΙΣΤΙΚΑ
# ========================================
class QuizStatistics(BaseModel):
    """Στατιστικά για ένα quiz"""
    quiz_id: int = Field(..., description="ID quiz")
    title: str = Field(..., description="Τίτλος quiz")
    total_attempts: int = Field(..., ge=0, description="Συνολικές προσπάθειες")
    completed_attempts: int = Field(..., ge=0, description="Ολοκληρωμένες προσπάθειες")
    passed_attempts: int = Field(..., ge=0, description="Επιτυχημένες προσπάθειες")
    average_score: float = Field(..., ge=0, le=100, description="Μέσος όρος βαθμολογίας")
    average_time_minutes: float = Field(..., ge=0, description="Μέσος χρόνος σε λεπτά")
    
    
    @property
    def pass_rate(self) -> float:
        """Ποσοστό επιτυχίας"""
        if self.completed_attempts == 0:
            return 0.0
        return round((self.passed_attempts / self.completed_attempts) * 100, 2)

class UserQuizProgress(BaseModel):
    """Πρόοδος μαθητή σε ένα quiz"""
    user_id: int = Field(..., description="ID μαθητή")
    quiz_id: int = Field(..., description="ID quiz")
    best_score: Optional[int] = Field(None, description="Καλύτερη βαθμολογία")
    best_percentage: Optional[int] = Field(None, ge=0, le=100, description="Καλύτερο ποσοστό")
    attempts_count: int = Field(..., ge=0, description="Αριθμός προσπαθειών")
    last_attempt_at: Optional[datetime] = Field(None, description="Τελευταία προσπάθεια")
    is_passed: bool = Field(False, description="Αν έχει περάσει το quiz")
    
    
    @property
    def remaining_attempts(self, max_attempts: int = 3) -> int:
        """Υπολειπόμενες προσπάθειες"""
        return max(0, max_attempts - self.attempts_count)

# ========================================
# 6. ΠΡΟΣΘΗΚΗ: ΣΧΗΜΑΤΑ ΓΙΑ ΦΙΛΤΡΑΡΙΣΜΑ
# ========================================
class QuizFilter(BaseModel):
    """Φίλτρα για αναζήτηση quizzes"""
    title_contains: Optional[str] = Field(None, description="Αναζήτηση στον τίτλο")
    lesson_id: Optional[int] = Field(None, description="Φιλτράρισμα κατά μάθημα")
    is_published: Optional[bool] = Field(None, description="Φιλτράρισμα κατά δημοσίευση")
    min_points: Optional[int] = Field(None, ge=0, description="Ελάχιστοι πόντοι")
    max_points: Optional[int] = Field(None, ge=0, description="Μέγιστοι πόντοι")
    created_after: Optional[datetime] = Field(None, description="Δημιουργήθηκε μετά από")
    created_before: Optional[datetime] = Field(None, description="Δημιουργήθηκε πριν από")
    has_questions: Optional[bool] = Field(True, description="Με τουλάχιστον μία ερώτηση")
    
    @field_validator('max_points')
    @classmethod
    def validate_points_range(cls, v: Optional[int], info) -> Optional[int]:
        """Ελέγχει ότι min_points <= max_points"""
        min_points = info.data.get('min_points')
        if min_points is not None and v is not None and min_points > v:
            raise ValueError("Το min_points δεν μπορεί να είναι μεγαλύτερο του max_points")
        return v