import numpy as np
from numpy import testing as np_testing
from scipy.linalg import expm, logm

from pymanopt.tools.multi import (
    multiexpm,
    multieye,
    multihconj,
    multilogm,
    multiprod,
    multisym,
    multitransp,
)

from ._test import TestCase


class TestMulti(TestCase):
    def setUp(self):
        self.m = 40
        self.n = 50
        self.p = 40
        self.k = 10

    def test_multiprod_singlemat(self):
        # Two random matrices A (m x n) and B (n x p)
        A = np.random.normal(size=(self.m, self.n))
        B = np.random.normal(size=(self.n, self.p))

        # Compare the products.
        np_testing.assert_allclose(A @ B, multiprod(A, B))

    def test_multiprod(self):
        # Two random arrays of matrices A (k x m x n) and B (k x n x p)
        A = np.random.normal(size=(self.k, self.m, self.n))
        B = np.random.normal(size=(self.k, self.n, self.p))

        C = np.zeros((self.k, self.m, self.p))
        for i in range(self.k):
            C[i] = A[i] @ B[i]

        np_testing.assert_allclose(C, multiprod(A, B))

    def test_multitransp_singlemat(self):
        A = np.random.normal(size=(self.m, self.n))
        np_testing.assert_array_equal(A.T, multitransp(A))

    def test_multitransp(self):
        A = np.random.normal(size=(self.k, self.m, self.n))

        C = np.zeros((self.k, self.n, self.m))
        for i in range(self.k):
            C[i] = A[i].T

        np_testing.assert_array_equal(C, multitransp(A))

    def test_multisym(self):
        A = np.random.normal(size=(self.k, self.m, self.m))

        C = np.zeros((self.k, self.m, self.m))
        for i in range(self.k):
            C[i] = 0.5 * (A[i] + A[i].T)

        np.testing.assert_allclose(C, multisym(A))

    def test_multieye(self):
        A = np.zeros((self.k, self.n, self.n))
        for i in range(self.k):
            A[i] = np.eye(self.n)

        np_testing.assert_allclose(A, multieye(self.k, self.n))

    def test_multilogm_singlemat(self):
        a = np.diag(np.random.uniform(size=self.m))
        q, _ = np.linalg.qr(np.random.normal(size=(self.m, self.m)))
        # A is a positive definite matrix
        A = q @ a @ q.T
        np_testing.assert_allclose(
            multilogm(A, positive_definite=True), logm(A)
        )

    def test_multilogm(self):
        A = np.zeros((self.k, self.m, self.m))
        L = np.zeros((self.k, self.m, self.m))
        for i in range(self.k):
            a = np.diag(np.random.uniform(size=self.m))
            q, _ = np.linalg.qr(np.random.normal(size=(self.m, self.m)))
            A[i] = q @ a @ q.T
            L[i] = logm(A[i])
        np_testing.assert_allclose(multilogm(A, positive_definite=True), L)

    def test_multilogm_complex_positive_definite(self):
        shape = (self.k, self.m, self.m)
        A = np.random.normal(size=shape) + 1j * np.random.normal(size=shape)
        A = multiprod(A, multihconj(A))
        # Compare fast path for positive definite matrices vs. general slow
        # one.
        np_testing.assert_allclose(
            multilogm(A, positive_definite=True),
            multilogm(A, positive_definite=False),
        )

    def test_multiexpm_singlemat(self):
        # A is a positive definite matrix
        A = np.random.normal(size=(self.m, self.m))
        A = A + A.T
        np_testing.assert_allclose(multiexpm(A, symmetric=True), expm(A))

    def test_multiexpm(self):
        A = multisym(np.random.normal(size=(self.k, self.m, self.m)))
        e = np.zeros((self.k, self.m, self.m))
        for i in range(self.k):
            e[i] = expm(A[i])
        np_testing.assert_allclose(multiexpm(A, symmetric=True), e)

    def test_multiexpm_conjugate_symmetric(self):
        shape = (self.k, self.m, self.m)
        A = np.random.normal(size=shape) + 1j * np.random.normal(size=shape)
        A = 0.5 * (A + multihconj(A))
        # Compare fast path for conjugate symmetric matrices vs. general slow
        # one.
        np_testing.assert_allclose(
            multiexpm(A, symmetric=True), multiexpm(A, symmetric=False)
        )
