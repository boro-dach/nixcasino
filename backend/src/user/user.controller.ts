import { Controller, Get, Post, Put, Body, Param } from '@nestjs/common';
import { UserService } from './user.service';
import { User } from 'generated/prisma/client';
import {
  CreateUserDto,
  UpdateBalanceDto,
  UpdateTurnoverDto,
} from './dto/user.dto';

@Controller('users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post()
  async create(@Body() dto: CreateUserDto): Promise<User> {
    return await this.userService.create(dto);
  }

  @Get(':id')
  async findById(@Param('id') id: string): Promise<User> {
    return await this.userService.findById(parseInt(id));
  }

  @Post(':id/get-or-create')
  async getOrCreate(
    @Param('id') id: string,
    @Body() body: { name: string },
  ): Promise<User> {
    return await this.userService.getOrCreate(parseInt(id), body.name);
  }

  @Put(':id/balance')
  async updateBalance(
    @Param('id') id: string,
    @Body() dto: UpdateBalanceDto,
  ): Promise<User> {
    return await this.userService.updateBalance(parseInt(id), dto.amount);
  }

  @Put(':id/turnover')
  async updateTurnover(
    @Param('id') id: string,
    @Body() dto: UpdateTurnoverDto,
  ): Promise<User> {
    return await this.userService.updateTurnover(parseInt(id), dto.amount);
  }

  @Put(':id/deposit')
  async deposit(
    @Param('id') id: string,
    @Body() dto: UpdateBalanceDto,
  ): Promise<User> {
    return await this.userService.updateDeposits(parseInt(id), dto.amount);
  }

  @Put(':id/withdraw')
  async withdraw(
    @Param('id') id: string,
    @Body() dto: UpdateBalanceDto,
  ): Promise<User> {
    return await this.userService.updateWithdrawals(parseInt(id), dto.amount);
  }

  @Get(':id/stats')
  async getStats(@Param('id') id: string): Promise<User> {
    return await this.userService.getStats(parseInt(id));
  }
}
