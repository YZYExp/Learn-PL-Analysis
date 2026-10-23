From Stdlib Require Import ZArith Vectors.Fin.

(* A finite-address, exclusive-ownership teaching model.
   This file does not import VST, Clight, or CompCert and does not prove
   any semax_body judgment about a C program. *)
Module HeapModel.
Section FiniteHeap.
Variable bound : nat.
Definition addr := Fin.t bound.
Definition heap := addr -> option Z.

Definition empty : heap := fun _ => None.
Definition read (h : heap) (p : addr) : option Z := h p.
Definition single (p : addr) (v : Z) : heap :=
  fun q => if Fin.eq_dec q p then Some v else None.

(* This total mathematical update is used only under an ownership precondition.
   It does not by itself model C allocation, alignment, or permissions. *)
Definition write (h : heap) (p : addr) (v : Z) : heap :=
  fun q => if Fin.eq_dec q p then Some v else h q.

Definition same (h1 h2 : heap) : Prop := forall p, h1 p = h2 p.
Definition disjoint (h1 h2 : heap) : Prop :=
  forall p, h1 p = None \/ h2 p = None.
Definition union (h1 h2 : heap) : heap :=
  fun p => match h1 p with Some v => Some v | None => h2 p end.

Definition assertion := heap -> Prop.
Definition points (p : addr) (v : Z) : assertion :=
  fun h => same h (single p v).
Definition sep (P Q : assertion) : assertion :=
  fun h => exists h1 h2,
    disjoint h1 h2 /\ same h (union h1 h2) /\ P h1 /\ Q h2.

Lemma single_here : forall p v, single p v p = Some v.
Proof.
  intros p v. unfold single. destruct (Fin.eq_dec p p); congruence.
Qed.

Lemma single_elsewhere : forall p q v,
    q <> p -> single p v q = None.
Proof.
  intros p q v H. unfold single. destruct (Fin.eq_dec q p); congruence.
Qed.

Theorem read_after_write : forall h p v,
    read (write h p v) p = Some v.
Proof.
  intros h p v. unfold read, write.
  destruct (Fin.eq_dec p p); congruence.
Qed.

Theorem read_other_after_write : forall h p q v,
    q <> p -> read (write h p v) q = read h q.
Proof.
  intros h p q v H. unfold read, write.
  destruct (Fin.eq_dec q p); congruence.
Qed.

Theorem separated_cell_excludes_alias : forall p old frame,
    disjoint (single p old) frame -> frame p = None.
Proof.
  intros p old frame H. specialize (H p).
  rewrite single_here in H. destruct H as [Hbad | Hgood].
  - discriminate.
  - exact Hgood.
Qed.

Theorem owned_read : forall p v R h,
    sep (points p v) R h -> read h p = Some v.
Proof.
  intros p v R h [h1 [h2 [Hd [He [Hp HR]]]]].
  unfold read. rewrite (He p). unfold union.
  unfold points, same in Hp. rewrite (Hp p), single_here.
  reflexivity.
Qed.

(* A concrete frame conclusion for the one-cell update command.
   R may be any predicate on the disjoint finite remainder heap. *)
Theorem write_owned_frame : forall p old new R h,
    sep (points p old) R h ->
    sep (points p new) R (write h p new).
Proof.
  intros p old new R h [h1 [h2 [Hd [He [Hp HR]]]]].
  assert (Hnone : h2 p = None).
  { specialize (Hd p). unfold points, same in Hp.
    rewrite (Hp p), single_here in Hd.
    destruct Hd as [Hbad | Hgood]; [discriminate | exact Hgood]. }
  exists (single p new), h2.
  split.
  - intros q. destruct (Fin.eq_dec q p) as [E | N].
    + subst q. right. exact Hnone.
    + left. apply single_elsewhere. exact N.
  - split.
    + intros q. unfold write, union.
      destruct (Fin.eq_dec q p) as [E | N].
      * subst q. rewrite single_here. reflexivity.
      * rewrite single_elsewhere by exact N.
        rewrite (He q). unfold union.
        unfold points, same in Hp. rewrite (Hp q).
        rewrite single_elsewhere by exact N. reflexivity.
    + split.
      * unfold points, same. intro q. reflexivity.
      * exact HR.
Qed.

(* Sharing the very same exclusive cell cannot satisfy separation. *)
Theorem no_duplicate_exclusive_ownership : forall p v w h,
    ~ sep (points p v) (points p w) h.
Proof.
  intros p v w h [h1 [h2 [Hd [He [Hp Hq]]]]].
  specialize (Hd p). unfold points, same in Hp, Hq.
  rewrite (Hp p), (Hq p), !single_here in Hd.
  destruct Hd; discriminate.
Qed.

End FiniteHeap.
Print Assumptions read_after_write.
Print Assumptions read_other_after_write.
Print Assumptions separated_cell_excludes_alias.
Print Assumptions owned_read.
Print Assumptions write_owned_frame.
Print Assumptions no_duplicate_exclusive_ownership.
End HeapModel.
