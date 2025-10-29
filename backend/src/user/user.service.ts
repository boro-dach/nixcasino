/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import { Injectable } from '@nestjs/common';
import { PrismaClient, User } from 'generated/prisma/client';
import { CreateUserDto } from './dto/user.dto';

@Injectable()
export class UserService {
  constructor(private readonly prisma: PrismaClient) {}

  async create(dto: CreateUserDto): Promise<User> {
    const user = await this.prisma.user.create({
      data: {
        id: dto.id,
        name: dto.name,
      },
    });
    return user;
  }

  async findById(id: number): Promise<User> {
    const user = await this.prisma.user.findFirst({
      where: { id },
    });
    return user;
  }

  async getOrCreate(id: number, name: string): Promise<User> {
    let user = await this.findById(id);

    if (!user) {
      user = await this.create({ id, name });
    }

    return user;
  }

  async updateBalance(id: number, amount: number): Promise<User> {
    return await this.prisma.user.update({
      where: { id },
      data: {
        balance: { increment: amount },
      },
    });
  }

  async updateTurnover(id: number, amount: number): Promise<User> {
    return await this.prisma.user.update({
      where: { id },
      data: {
        turnover: { increment: amount },
        gamesPlayed: { increment: 1 },
      },
    });
  }

  async updateDeposits(id: number, amount: number): Promise<User> {
    return await this.prisma.user.update({
      where: { id },
      data: {
        totalDeposits: { increment: amount },
        balance: { increment: amount },
      },
    });
  }

  async updateWithdrawals(id: number, amount: number): Promise<User> {
    return await this.prisma.user.update({
      where: { id },
      data: {
        totalWithdrawals: { increment: amount },
        balance: { decrement: amount },
      },
    });
  }

  async getStats(id: number): Promise<User> {
    return await this.prisma.user.findFirst({
      where: { id },
    });
  }
}
