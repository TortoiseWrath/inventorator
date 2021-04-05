import {Decimal} from '@/types/Decimal';
import {Link} from '@/types/Link';
import {Item} from '@/types/Item';

export interface ItemDetails extends Item {
    description?: string,
    acquired?: Date,
    basis?: Decimal,
    valueAsOf?: Date,
    upc?: string,
    d1?: Decimal,
    d2?: Decimal,
    d3?: Decimal,
    photos?: string[],
    links?: Link[],
    created: Date,
    modified: Date,
}