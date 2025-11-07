import { IsEnum, IsNumber, IsString } from 'class-validator';
import { Games, Results } from 'generated/prisma';

export class GameResultDto {
  @IsString()
  userId: string;

  @IsEnum(Games)
  game: Games;

  @IsEnum(Results)
  result: Results;

  @IsNumber()
  profit: number;
}
