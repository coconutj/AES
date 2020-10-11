# -*- coding: utf-8 -*-
"""
    Created: 10/11/2020
    Last modification: 10/11/2020

    @creator: coconutj

    Brief: Toy Implementation of functions for AES Cipher
"""

#-- Import --#
from constants import *
#- End Import -#

def SubBytes(state):
    """
    SubBytes operation
    - input: (ByteMatrix object) state
    - output: (ByteMatrix object) state
    """
    try:
        assert type(state) == ByteMatrix

        for i in range(state.m):
            for j in range(state.n):
                state[i,j] = Byte(SBox[state[i,j].byte])

        return state
    except AssertionError:
        raise TypeError("Argument must be of type ByteMatrix.")

def ShiftRows(state):
    """
    ShiftRows operation
    - input: (4x4 ByteMatrix object) state
    - output: (4x4 ByteMatrix object) state
    """
    try:
        assert type(state) == ByteMatrix
        assert (state.m == 4) and (state.n == 4)

        state << (1,1)
        state << (2,2)
        state << (3,3)

        return state
    except AssertionError:
        raise ValueError("Argument must be of type ByteMatrix of size 4x4.")    

def MixColumns(state):
    """
    MixColumns operation
    - input: (4x4 ByteMatrix object) state
    - output: (4x4 ByteMatrix object) state
    """
    try:
        assert type(state) == ByteMatrix
        assert (state.m == 4) and (state.n == 4)

        state = MixColumns_mat * state

        return state
    except AssertionError:
        raise ValueError("Argument must be of type ByteMatrix of size 4x4.")

def AddRoundKey(state, round_key):
    """
    MixColumns operation
    - input: (4x4 ByteMatrix object) state, (4x4 ByteMatrix object) round_key
    - output: (4x4 ByteMatrix object) state
    """
    try:
        assert (type(state) == ByteMatrix) and (type(round_key) == ByteMatrix)
        assert (state.m == 4) and (state.n == 4) and (round_key.m == 4) and (round_key.n == 4)

        state += round_key

        return state
    except AssertionError:
        raise ValueError("Arguments must be of type ByteMatrix of size 4x4.")    

def InvSubBytes(state):
    """
    SubBytes operation
    - input: (ByteMatrix object) state
    - output: (ByteMatrix object) state
    """
    try:
        assert type(state) == ByteMatrix

        for i in range(state.m):
            for j in range(state.n):
                state[i,j] = Byte(InvSBox[state[i,j].byte])

        return state
    except AssertionError:
        raise TypeError("Argument must be of type ByteMatrix.")

def InvShiftRows(state):
    """
    ShiftRows operation
    - input: (4x4 ByteMatrix object) state
    - output: (4x4 ByteMatrix object) state
    """
    try:
        assert type(state) == ByteMatrix
        assert (state.m == 4) and (state.n == 4)

        state >> (1,1)
        state >> (2,2)
        state >> (3,3)

        return state
    except AssertionError:
        raise ValueError("Argument must be of type ByteMatrix of size 4x4.")    

def InvMixColumns(state):
    """
    InvMixColumns operation
    - input: (4x4 ByteMatrix object) state
    - output: (4x4 ByteMatrix object) state
    """
    try:
        assert type(state) == ByteMatrix
        assert (state.m == 4) and (state.n == 4)

        state = InvMixColumns_mat * state

        return state
    except AssertionError:
        raise ValueError("Argument must be of type ByteMatrix of size 4x4.")

def RotWord(word):
    """
    RotWord operation
    - input: (4x1 ByteMatrix object) word
    - output: (4x1 ByteMatrix object) word
    """
    try:
        assert type(word) == ByteMatrix
        assert (word.m == 4) and (word.n == 1)

        tmp = word[0,0]
        word[0,0] = word[1,0]
        word[1,0] = word[2,0]
        word[2,0] = word[3,0]
        word[3,0] = tmp

        return word
    except AssertionError:
        raise ValueError("Argument must be of type ByteMatrix of size 4x1")

def KeyExpansion(key, listed=True):
    """
    KeyExpansion algorithm
    - input: (bytes) key
    - output: (ByteMatrix) W
    """
    try:
        assert type(key) == bytes
    except:
        raise TypeError("Key must be of type bytes (built-in)")
    # Key size in bytes
    key_size = len(key)
    if key_size < 16:
        key = (16 - key_size)*b'\x00' + key
        key_size = 16
    elif 16 < key_size < 24:
        key = (24 - key_size)*b'\x00' + key
        key_size = 24
    elif 24 < key_size < 32:
        key = (32 - key_size)*b'\x00' + key
        key_size = 32
    Nk = key_size // 4
    Nr = 10 + (Nk - 4)

    W = zeros((4,4*(Nr+1)))

    i,j = 0,0
    for key_byte in key:
        W[i,j] = Byte(key_byte)
        i,j = (0,j+1) if (i == 3) else (i+1, j)

    for j in range(Nk, 4*(Nr+1)):
        if (j%Nk == 0):
            W[:, j] = W[:, j-Nk] + SubBytes(RotWord(W[:, j-1])) + Rcon[:, j // Nk - 1]
        elif (Nk > 6) and (j%Nk == 4):
            W[:, j] = W[:, j-Nk] + SubBytes(W[:, j-1])
        else:
            W[:, j] = W[:, j-Nk] + W[:, j-1]

    if listed:
        l = []
        for j in range(Nr+1):
            round_key = zeros((4,4))
            for k in range(4):
                round_key[:,k] = W[:, 4*j + k]
            l.append(round_key)
        return l
    else:
        return W

def Enc(block, key):
    """
    AES cipher
    - input: (bytes, 16 B) block, (bytes) key
    - output: (bytes, 16 B) ciphertext
    """
    state = bytes2ByteMatrix(block)
    W_list = KeyExpansion(key, listed=True)
    Nr = len(W_list) - 1

    # First round
    state = AddRoundKey(state, W_list[0])

    # Middle rounds
    for i in range(1, Nr):
        state = AddRoundKey(MixColumns(ShiftRows(SubBytes(state))), W_list[i])

    # Final round
    state = AddRoundKey(ShiftRows(SubBytes(state)), W_list[Nr])

    return ByteMatrix2bytes(state)

def Dec(block, key):
    """
    AES inverse cipher
    - input: (bytes, 16 B) block, (bytes) key
    - output: (bytes, 16 B) ciphertext
    """
    state = bytes2ByteMatrix(block)
    W_list = KeyExpansion(key, listed=True)
    Nr = len(W_list) - 1

    # First round
    state = AddRoundKey(state, W_list[Nr])

    # Middle rounds
    for i in range(Nr-1, 0, -1):
        state = InvMixColumns(AddRoundKey(InvSubBytes(InvShiftRows(state)), W_list[i]))

    # Final round
    state = AddRoundKey(InvSubBytes(InvShiftRows(state)), W_list[0])

    return ByteMatrix2bytes(state)