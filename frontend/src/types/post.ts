interface Post {
    id: number;
    title: string;
    content: string;
    author: {
        username: string;
    };
    createdAt: string;
    views_count: number;
    likes_count: number;
    replies: {
        items: Reply[];
        total: number;
        pages: number;
        current_page: number;
        per_page: number;
        has_next: boolean;
        has_prev: boolean;
    };
}

interface Reply {
    id: number;
    content: string;
    author: {
        username: string;
    };
    createdAt: string;
    likes_count: number;
}

export type { Post, Reply };