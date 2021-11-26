#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bot import dp
from aiogram.utils import executor

def main():
    """Основная программа"""
    executor.start_polling(dp)

# Стартовая точка прогаммы
if __name__ == "__main__":
    main()
