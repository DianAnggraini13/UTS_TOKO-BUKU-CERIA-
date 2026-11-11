
from pydantic import BaseModel, Field
from typing import Optional


# Skema untuk menambahkan buku
class BukuCreate(BaseModel):
    judul: str = Field(min_length=1)
    penulis: str = Field(min_length=1)
    kategori: str = Field(min_length=1)
    harga: float = Field(ge=0)
    stok: int = Field(ge=0)


# Skema untuk memperbarui buku
class BukuUpdate(BaseModel):
    judul: Optional[str] = Field(default=None, min_length=1)
    penulis: Optional[str] = Field(default=None, min_length=1)
    kategori: Optional[str] = Field(default=None, min_length=1)
    harga: Optional[float] = Field(default=None, ge=0)
    stok: Optional[int] = Field(default=None, ge=0)


# Skema untuk response data buku
class BukuResponse(BaseModel):
    id: int
    judul: str
    penulis: str
    kategori: str
    harga: float
    stok: int


# Skema untuk membuat transaksi
class TransactionCreate(BaseModel):
    buku_id: int = Field(gt=0)
    jumlah: int = Field(gt=0)


# Skema untuk response transaksi
class TransactionResponse(BaseModel):
    id: int
    buku_id: int
    jumlah: int
    status: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    error_message: Optional[str] = None
