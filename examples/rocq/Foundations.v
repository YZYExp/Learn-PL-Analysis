From Stdlib Require Import Lists.List Arith.PeanoNat.
Import ListNotations.

(* Rocq 9.0.0, using only the core and Stdlib.
   Finite boolean lists model entries, not unique payment requests. *)
Module RocqFoundations.

Theorem and_swap (P Q : Prop) : P /\ Q -> Q /\ P.
Proof.
  intros [hp hq].
  split.
  - exact hq.
  - exact hp.
Qed.

Theorem implication_chain (P Q R : Prop)
    (hpq : P -> Q) (hqr : Q -> R) : P -> R.
Proof.
  intro hp.
  exact (hqr (hpq hp)).
Qed.

Fixpoint two_per_item (n : nat) : nat :=
  match n with
  | 0 => 0
  | S k => S (S (two_per_item k))
  end.

Theorem two_per_item_eq_add :
  forall n : nat, two_per_item n = n + n.
Proof.
  induction n as [|k IH].
  - reflexivity.
  - change (S (S (two_per_item k)) = S (k + S k)).
    rewrite IH.
    rewrite Nat.add_succ.
    reflexivity.
Qed.

Fixpoint accepted_count (xs : list bool) : nat :=
  match xs with
  | [] => 0
  | b :: rest =>
      if b then S (accepted_count rest) else accepted_count rest
  end.

Theorem accepted_count_le_length :
  forall xs : list bool, accepted_count xs <= length xs.
Proof.
  induction xs as [|b rest IH].
  - exact (Nat.le_refl 0).
  - destruct b.
    + cbn [accepted_count length].
      exact (@le_n_S _ _ IH).
    + cbn [accepted_count length].
      exact (@le_S _ _ IH).
Qed.

Example accepted_count_sample :
  accepted_count [true; false; true] = 2.
Proof. reflexivity. Qed.

Compute accepted_count [true; false; true].
Print Assumptions and_swap.
Print Assumptions implication_chain.
Print Assumptions two_per_item_eq_add.
Print Assumptions accepted_count_le_length.
Print Assumptions accepted_count_sample.

End RocqFoundations.
