import {Decimal} from '@/types/Decimal';

export interface Item {
    title: string,
    childCount: number,
    value?: Decimal,
    weight?: Decimal,
    volume?: Decimal,
    totalValue?: Decimal,
    totalWeight?: Decimal,
    totalVolume?: Decimal,
    id: number,
    parent: number,
    expanded?: boolean, // null at first, then true or false after first expanded
}

