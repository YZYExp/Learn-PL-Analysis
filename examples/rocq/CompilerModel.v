(* Independent teaching model, NOT the CompCert compiler or its proof.
   Rocq 9.0.0 + Stdlib only. Natural numbers have no machine overflow.
   Expressions are total and pure: no memory, I/O, exceptions or divergence. *)
From Stdlib Require Import Arith.PeanoNat.

Module CompilerModel.

Inductive expr : Type :=
| Lit : nat -> expr
| Var : nat -> expr
| Add : expr -> expr -> expr.

Definition env := nat -> nat.

Fixpoint eval (rho : env) (e : expr) : nat :=
  match e with
  | Lit n => n
  | Var x => rho x
  | Add a b => eval rho a + eval rho b
  end.

(* Fold two constants; otherwise remove only a literal zero on the right. *)
Definition smart_add (a b : expr) : expr :=
  match a, b with
  | Lit n, Lit m => Lit (n + m)
  | _, Lit 0 => a
  | _, _ => Add a b
  end.

Lemma eval_smart_add : forall rho a b,
  eval rho (smart_add a b) = eval rho a + eval rho b.
Proof.
  intros rho a b.
  destruct a as [n | x | a1 a2];
  destruct b as [m | y | b1 b2];
  simpl; try reflexivity.
  all: destruct m; simpl; rewrite ?Nat.add_0_r; reflexivity.
Qed.

Fixpoint optimize (e : expr) : expr :=
  match e with
  | Lit n => Lit n
  | Var x => Var x
  | Add a b => smart_add (optimize a) (optimize b)
  end.

Theorem optimize_correct : forall rho e,
  eval rho (optimize e) = eval rho e.
Proof.
  intros rho e.
  induction e as [n | x | a IHa b IHb]; cbn [optimize].
  - reflexivity.
  - reflexivity.
  - rewrite eval_smart_add. cbn [eval].
    rewrite IHa, IHb. reflexivity.
Qed.

Definition observes (rho : env) (e : expr) (n : nat) : Prop :=
  eval rho e = n.

Corollary optimize_observations : forall rho e n,
  observes rho (optimize e) n <-> observes rho e n.
Proof.
  intros rho e n. unfold observes.
  rewrite optimize_correct. reflexivity.
Qed.

Definition demo : expr :=
  Add (Add (Var 0) (Lit 0)) (Add (Lit 2) (Lit 3)).

Example demo_shape : optimize demo = Add (Var 0) (Lit 5).
Proof. reflexivity. Qed.

Example demo_value : eval (fun _ => 10) (optimize demo) = 15.
Proof. reflexivity. Qed.

(* Check the actual dependency reports, not just that Qed was accepted. *)
Print Assumptions eval_smart_add.
Print Assumptions optimize_correct.
Print Assumptions optimize_observations.
Print Assumptions demo_shape.
Print Assumptions demo_value.

End CompilerModel.
