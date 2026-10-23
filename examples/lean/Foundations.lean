import Std

/-
  Foundations for the book's formal-proof introduction.
  Toolchain: Lean 4.19.0; only Lean core and Std.
  Models use Nat and List Bool, not machine integers or payment services.
-/
namespace Foundations

/-- Reordering two independently supplied pieces of evidence. -/
theorem and_swap (P Q : Prop) : P ∧ Q → Q ∧ P := by
  intro h
  constructor
  · exact h.2
  · exact h.1

/-- Compose two implications; no assumption that P itself is true. -/
theorem implication_chain (P Q R : Prop)
    (hpq : P → Q) (hqr : Q → R) : P → R := by
  intro hp
  exact hqr (hpq hp)

/-- Add two counters for each item. This definition is structurally recursive. -/
def twoPerItem : Nat → Nat
  | 0 => 0
  | Nat.succ n => Nat.succ (Nat.succ (twoPerItem n))

/-- The base case and step case cover every natural number. -/
theorem twoPerItem_eq_add (n : Nat) : twoPerItem n = n + n := by
  induction n with
  | zero => rfl
  | succ k ih =>
      -- ih : twoPerItem k = k + k
      -- target: twoPerItem (Nat.succ k) = Nat.succ k + Nat.succ k
      calc
        twoPerItem (Nat.succ k) = Nat.succ (Nat.succ (twoPerItem k)) := rfl
        _ = Nat.succ (Nat.succ (k + k)) :=
          congrArg (fun x => Nat.succ (Nat.succ x)) ih
        _ = Nat.succ (k + Nat.succ k) :=
          congrArg Nat.succ (Nat.add_succ k k).symm
        _ = Nat.succ k + Nat.succ k :=
          (Nat.succ_add k (Nat.succ k)).symm

/-- Count accepted entries in a finite list, not distinct business requests. -/
def acceptedCount : List Bool → Nat
  | [] => 0
  | true :: xs => Nat.succ (acceptedCount xs)
  | false :: xs => acceptedCount xs

/-- An acceptance counter never exceeds the number of list entries. -/
theorem acceptedCount_le_length (xs : List Bool) :
    acceptedCount xs ≤ xs.length := by
  induction xs with
  | nil =>
      exact Nat.le_refl 0
  | cons b xs ih =>
      cases b with
      | false =>
          -- Target reduces to acceptedCount xs ≤ Nat.succ xs.length.
          exact Nat.le_trans ih (Nat.le_succ xs.length)
      | true =>
          -- Both sides gain one; use the induction hypothesis.
          exact Nat.succ_le_succ ih

-- Finite computation is useful evidence, but not a universal proof.
#eval acceptedCount [true, false, true]

-- These print the actual foundational dependencies after kernel checking.
#print axioms and_swap
#print axioms implication_chain
#print axioms twoPerItem_eq_add
#print axioms acceptedCount_le_length

end Foundations
