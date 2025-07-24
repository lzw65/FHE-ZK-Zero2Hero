# Paillier同态加密系统详解
[Kurt Pan全同态加密和隐私互联网的黎明](https://mp.weixin.qq.com/s/mjUBh_HdprBeKUUvtdid6w)以极简方式从头开始构建
以下是基于Paillier加密方案的Python实现，支持同态加法运算。让我们逐步解析每个函数的功能和数学原理：

## 1. 密钥生成函数 `generate_keypair`

```python
def generate_keypair(bit_length=512):
    p = sympy.nextprime(random.getrandbits(bit_length))
    q = sympy.nextprime(random.getrandbits(bit_length))
    n = p * q
    g = n + 1
    lambda_ = (p - 1) * (q - 1)
    mu = sympy.mod_inverse(lambda_, n)
    return (n, g), (lambda_, mu)
```

### 数学原理：
- **生成大素数**：随机生成两个`bit_length`位的大素数`p`和`q`
- **计算模数**：`n = p × q`（RSA模数）
- **选择生成元**：`g = n + 1`（Paillier系统的标准选择）
- **计算Carmichael函数**：`λ = lcm(p-1, q-1) = (p-1)(q-1)`（因为p,q是素数）
- **计算模逆元**：`μ = λ⁻¹ mod n`（用于解密）

### 返回值：
- **公钥**：`(n, g)`
- **私钥**：`(λ, μ)`

## 2. 加密函数 `encrypt`

```python
def encrypt(m, public_key):
    n, g = public_key
    r = random.randint(1, n - 1)
    return (pow(g, m, n**2) * pow(r, n, n**2)) % (n**2)
```

### 加密过程：
- **输入**：明文`m`，公钥`(n, g)`
- **选择随机数**：`r ∈ [1, n-1]`（保证加密的随机性）
- **计算密文**：`c = gᵐ × rⁿ mod n²`
- 使用`g = n+1`的特殊性质简化计算
- 模`n²`保证结果在正确范围内

## 3. 解密函数 `decrypt`

```python
def decrypt(c, private_key, public_key):
    lambda_, mu = private_key
    n, _ = public_key
    l = (pow(c, lambda_, n**2) - 1) // n
    return (l * mu) % n
```

### 解密过程：
- **计算L函数**：`L(u) = (u-1)/n`
- **中间值计算**：`l = L(c^λ mod n²)`
- **恢复明文**：`m = (l × μ) mod n`

### 数学基础：
利用以下恒等式：

```
g^λ ≡ 1 mod n
c^λ ≡ g^{mλ} × r^{nλ} ≡ 1^m × 1 ≡ 1 mod n²
```

## 4. 同态加法函数 `homomorphic_sum`

```python
def homomorphic_sum(a, b, public_key):
    return (a * b) % (public_key[0]**2)
```

### 同态性质：
- **输入**：两个密文`a = E(m₁)`，`b = E(m₂)`
- **输出**：`E(m₁ + m₂)`
- **操作**：`c = a × b mod n²`

### 数学证明：
```
a × b = (gᵐ¹ × r₁ⁿ) × (gᵐ² × r₂ⁿ) mod n²
       = gᵐ¹⁺ᵐ² × (r₁r₂)ⁿ mod n²
       = E(m₁ + m₂)
```

## 5. 示例运行分析

```python
public_key, private_key = generate_keypair(128)
enc1 = encrypt(5, public_key)  # 加密5
enc2 = encrypt(3, public_key)  # 加密3
enc_sum = homomorphic_sum(enc1, enc2, public_key)  # 同态相加
dec_sum = decrypt(enc_sum, private_key, public_key)  # 解密得8
```

### 关键点：
- **同态性**：直接在密文上运算，无需解密
- **安全性**：基于复合剩余类问题（DCR）的困难性

### 应用场景：
- 隐私保护的数据聚合
- 安全多方计算
- 加密数据库查询

## 安全注意事项

- 实际应用中应使用加密安全的随机数生成器
- 对于大素数生成，推荐使用更强的素性检测算法
- 明文空间应限制在`[0, n)`范围内
- 128位密钥仅用于演示，实际应用需要至少2048位

---

Paillier系统因其加法同态性和相对高效性，在隐私计算领域有广泛应用。这种加密方式允许在不解密的情况下对加密数据进行运算，为安全数据处理提供了强大工具。