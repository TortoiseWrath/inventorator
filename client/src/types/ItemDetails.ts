import {Link} from '@/types/Link';
import {Item} from '@/types/Item';

export interface ItemDetails extends Item {
    description?: string,
    acquired?: string,
    basis?: string,
    valueAsOf?: string,
    upc?: string,
    d1?: string,
    d2?: string,
    d3?: string,
    photos?: string[],
    links?: Link[],
    created?: string,
    modified?: string,
}