import Std

/-!
Tiny models for chapters with stable IDs 40–42.
Target toolchain: Lean 4.19.0; core/Std only.
These theorems do not verify the Python analyzer, a payment service,
the Lean compiler, or execution on actual hardware.
-/
namespace ProgramProofs

-- Natural-number subtraction truncates at zero. The hypothesis matters.
def remaining (paid amount : Nat) : Nat := paid - amount

theorem refund_conservation (paid amount : Nat) (h : amount ≤ paid) :
    remaining paid amount + amount = paid := by
  exact Nat.sub_add_cancel h

inductive State where
  | paid
  | refunded
  deriving DecidableEq, Repr

def refundStep : State → Option State
  | .paid => some .refunded
  | .refunded => none

theorem first_request : refundStep .paid = some .refunded := by rfl

theorem repeated_request : refundStep .refunded = none := by rfl

-- Count successful transitions during a finite sequence of identical requests.
def successes : Nat → State → Nat
  | 0, _ => 0
  | n + 1, s =>
      match refundStep s with
      | none => successes n s
      | some s' => 1 + successes n s'

theorem refunded_successes (n : Nat) : successes n .refunded = 0 := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [successes, refundStep] using ih

theorem paid_successes (n : Nat) : successes (n + 1) .paid = 1 := by
  simp [successes, refundStep, refunded_successes]

theorem at_most_one (n : Nat) (s : State) : successes n s ≤ 1 := by
  cases s with
  | paid =>
      cases n with
      | zero => simp [successes]
      | succ n => simp [paid_successes]
  | refunded => simp [refunded_successes]

-- Pure, total natural-number functions. No evaluation effects or overflow.
def before (x : Nat) : Nat := (x + 0) + 1
def after (x : Nat) : Nat := x + 1

theorem remove_zero_correct (x : Nat) : before x = after x := by
  simp [before, after]

-- A two-element abstract domain for integers.
-- nonneg represents { z | 0 ≤ z }; any represents all integers.
inductive Abs where
  | nonneg
  | any
  deriving DecidableEq, Repr

def gamma : Abs → Int → Prop
  | .nonneg, z => 0 ≤ z
  | .any, _ => True

def incAbs : Abs → Abs
  | .nonneg => .nonneg
  | .any => .any

def inc (z : Int) : Int := z + 1

theorem inc_sound (a : Abs) (z : Int) (hz : gamma a z) :
    gamma (incAbs a) (inc z) := by
  cases a with
  | nonneg =>
      change 0 ≤ z at hz
      change 0 ≤ z + 1
      omega
  | any => trivial

def runConcrete : Nat → Int → Int
  | 0, z => z
  | n + 1, z => runConcrete n (inc z)

def runAbstract : Nat → Abs → Abs
  | 0, a => a
  | n + 1, a => runAbstract n (incAbs a)

theorem run_sound (n : Nat) (a : Abs) (z : Int) (hz : gamma a z) :
    gamma (runAbstract n a) (runConcrete n z) := by
  induction n generalizing a z with
  | zero => exact hz
  | succ n ih =>
      change gamma (runAbstract n (incAbs a)) (runConcrete n (inc z))
      exact ih (incAbs a) (inc z) (inc_sound a z hz)

#print axioms refund_conservation
#print axioms at_most_one
#print axioms remove_zero_correct
#print axioms inc_sound
#print axioms run_sound

end ProgramProofs
